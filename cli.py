import pymorphy2
import re
import sys


from pyswip import Prolog

morph = pymorphy2.MorphAnalyzer()
NAME_TAG = 'Name'
NAME_THRESHOLD = 0.2

IS_P1_R_P2 = 0
P_R_FORWARD = 1
P_R_BACKWARD = 2
WHICH_P_R_P = 3
ADD_P1_R_P2 = 4

UNKNOWN_COMMAND = -1

P_R_BACKWARD_MARKERS = {'кто', 'кем'}

INCORRECT_REQUEST = '!! Некорректный формат запроса !!'
NOT_ALLOWED = '!! Это отношение нельзя добавить !!'
EMPTY_RESULT = 'Нет данных по данному запросу'
SUCSESSFULLY_ADDED = 'Успешно добавлно'
ADD_ERROR = '!! Ошабка добавления !!'

PROMPT = '? >> '
BYE = '\nhalt'

ADD_PREFIX = 'ДОБАВИТЬ'

ALLOWED_TO_ADD = { 'отец', 'мать', 'сын', 'дочь', 'брат', 'сестра', 'муж',
    'жена', 'супруг', 'супруга'
}

RELATIONS = {
    'отец', 'мать', 'сын', 'дочь', 'ребенок', 'бабушка', 'дедушка',
    'прабабушка', 'прадедушка', 'дядя', 'тетя', 'кузен', 'кузина',
    'внук', 'внучка', 'правнук', 'правнучка', 'муж', 'жена', 'брат', 'сестра',
    'ребенок', 'ребёнок'
}

WORDS_REPL = {
    "матерь": "мать"
}

def restore_capital(name, word):
    if name[0].isupper():
        return word.capitalize()
    else:
        return word


def is_name(name):
    p = morph.parse(name)[0]
    if NAME_TAG in p.tag and p.score > NAME_THRESHOLD:
        return True
    return False


def get_genetive_case(name):
    p = morph.parse(name)[0]
    return restore_capital(name, p.inflect({'gent'}).word)


def get_norm_form_check_is_name(name):
    p = morph.parse(name)[0]
    norm = p.normal_form
    is_name = NAME_TAG in p.tag and p.score > NAME_THRESHOLD
    if is_name:
        norm = norm.capitalize()
    return norm, is_name


def get_relation(p1, p2, prolog):
    return


def filter_word(word):
    return ''.join(filter(lambda c: c.isalpha(), word.lower()))


def get_sensible_word(word):
    norm, is_name = get_norm_form_check_is_name(word)
    # for word which normalize incorrect, such as
    # матерью -> матерь
    if norm in WORDS_REPL:
        norm = WORDS_REPL[norm]
    if is_name or norm in RELATIONS:
        return norm
    return ''


def filter_request(request):
    sensible = map(get_sensible_word, request)

    return list(filter(lambda c: c != '', sensible))


def is_backward_request(request):
    is_kto = False
    for word in request:
        if word in P_R_BACKWARD_MARKERS:
            is_kto = True
    return is_kto


def parse_len_2_request(request, is_kto):
    a1, a2 = request

    if a1 not in RELATIONS and a2 not in RELATIONS:
        return (WHICH_P_R_P, a1, a2)
    if a1 not in RELATIONS and a2 in RELATIONS:
        if is_kto:
            return (P_R_BACKWARD, a2, a1)
        else:
            return (P_R_FORWARD, a2, a1)
    if a1 in RELATIONS and a2 not in RELATIONS:
        if is_kto:
            return (P_R_BACKWARD, a1, a2)
        else:
            return (P_R_FORWARD, a1, a2)


def parse_len_3_request(request, is_add):
    a1, a2, a3 = request
    if is_add:
        command = ADD_P1_R_P2
    else:
        command = IS_P1_R_P2

    if a1 in RELATIONS and a2 not in RELATIONS and a3 not in RELATIONS:
        if is_add:
            if a1 in ALLOWED_TO_ADD:
                return (command, a1, a3, a2)
            return (UNKNOWN_COMMAND, NOT_ALLOWED)
        else:
            return (command, a1, a3, a2)
    if a1 not in RELATIONS and a2 in RELATIONS and a3 not in RELATIONS:
        if is_add:
            if a2 in ALLOWED_TO_ADD:
                return (command, a2, a1, a3)
            return (UNKNOWN_COMMAND, NOT_ALLOWED)
        else:
            return (command, a2, a1, a3)
    if a1 not in RELATIONS and a2 not in RELATIONS and a3 in RELATIONS:
        if is_add:
            if a3 in ALLOWED_TO_ADD:
                return (command, a3, a1, a2)
            return (UNKNOWN_COMMAND, NOT_ALLOWED)
        else:
            return (command, a3, a1, a2)


def parse_command(s):
    is_add = False
    is_kto = False

    l = s.split(' ')
    if l[0] == ADD_PREFIX:
        is_add = True
        l = l[1:]

    l = list(map(filter_word, l))
    is_kto = is_backward_request(l)
    request = filter_request(l)

    command = (UNKNOWN_COMMAND, INCORRECT_REQUEST)

    if len(request) == 2:
        command = parse_len_2_request(request, is_kto)

    if len(request) == 3:
        command = parse_len_3_request(request, is_add)

    return command


def is_relation_between(rel, p1, p2, prolog):
    return len(list(prolog.query("{}('{}', '{}')".format(rel, p1, p2)))) > 0


def get_forward_objects(rel, p, prolog):
    return [i['X'] for i in prolog.query("{}('{}', X)".format(rel, p))]


def get_backward_objects(rel, p, prolog):
    return [i['X'] for i in prolog.query("{}(X, '{}')".format(rel, p))]


def get_relation_between(p1, p2, prolog):
    prolog_response = list(prolog.query("short_path('{}', '{}', X)".format(p1, p2)))
    if len(prolog_response) == 0:
        return []
    else:
        return list(map(str, prolog_response[0]['X']))


def add_relation(rel, p1, p2, prolog):
    return list(prolog.query("добавить_{}('{}', '{}')".format(rel, p1, p2)))


def prettify_relation_list(rel, o1, o2):
    res = ""
    if isinstance(o1, list):
        o2 = get_genetive_case(o2)
        for o in o1:
            res += "{} {} {}\n".format(o, rel, o2)
    else:
        for o in o2:
            res += "{} {} {}\n".format(o1, rel, get_genetive_case(o))

    return res[:-1]



def run_command(command, prolog):
    if command[0] == UNKNOWN_COMMAND:
        return command[1]
    if command[0] == IS_P1_R_P2:
        result = is_relation_between(command[1], command[2], command[3], prolog)
        if result:
            return 'Да'
        else:
            return 'Нет'
    if command[0] == P_R_FORWARD:
        result = get_forward_objects(command[1], command[2], prolog)
        if len(result) > 0:
            return prettify_relation_list(command[1], command[2], result)
        else:
            return EMPTY_RESULT
    if command[0] == P_R_BACKWARD:
        result = get_backward_objects(command[1], command[2], prolog)
        if len(result) > 0:
            return prettify_relation_list(command[1], result, command[2])
        else:
            return EMPTY_RESULT
    if command[0] == WHICH_P_R_P:
        result = get_relation_between(command[1], command[2], prolog)
        if len(result) > 0:
            return prettify_relation(result)
        else:
            return EMPTY_RESULT
    if command[0] == ADD_P1_R_P2:
        result = add_relation(command[1], command[2], command[3], prolog)
        if len(result) > 0:
            return SUCSESSFULLY_ADDED
        else:
            return ADD_ERROR


def prettify_relation(prolog_response):
    res = ""

    is_form = False
    for (ind, term) in enumerate(prolog_response):
        if ind == 0:
            res += term
            res += ' --'
        elif ind % 2 == 1:
            if not is_form:
                res += term
                is_form = True
            else:
                res += get_genetive_case(term)
        else:
            res += get_genetive_case(term)
            res += ','
        res += ' '

    return res[:-2]


def main():
    prolog = Prolog()
    prolog.consult("prolog/utils.pl")
    prolog.consult("prolog/setters.pl")
    prolog.consult("prolog/database.pl")
    prolog.consult("prolog/relations.pl")
    while(1):
        try:
            line = input(PROMPT)
            command = parse_command(line)
            result = run_command(command, prolog)
            print(result)
        except EOFError:
            print(BYE)
            break

if __name__ == "__main__":
    main()
