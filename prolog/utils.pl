:- ensure_loaded(database).
:- ensure_loaded(relations).
:- ensure_loaded(setters).

short_path(X, Y, L) :-
  wide_search([[X]], Y, L).
wide_search([[Y|T_one]|T], Y, L) :-
  !,
  length([Y|T_one], Len),
  wide_search1([[Y|T_one]|T], Len, Y, L).
wide_search([Path|T], Y, L) :-
  findall(X, next_one(Path, X), Paths),
  !,
  append(T, Paths, Paths_new),
  wide_search(Paths_new, Y, L).
next_one([Y|T], [X, 'сын', Y|T]) :-
  сын(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'дочь', Y|T]) :-
  дочь(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'брат', Y|T]) :-
  брат(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'сестра', Y|T]) :-
  сестра(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'отец', Y|T]) :-
  отец(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'мать', Y|T]) :-
  мать(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'дедушка', Y|T]) :-
  дедушка(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'бабушка', Y|T]) :-
  бабушка(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'муж', Y|T]) :-
  муж(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'жена', Y|T]) :-
  жена(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'внук', Y|T]) :-
  внук(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'внучка', Y|T]) :-
  внучка(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'дядя', Y|T]) :-
  дядя(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'тетя', Y|T]) :-
  тетя(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'кузен', Y|T]) :-
  кузен(Y, X),
  not(member(X, T)).
next_one([Y|T], [X, 'кузина', Y|T]) :-
  кузина(Y, X),
  not(member(X, T)).
wide_search1([[Y|Path]|_], Len, Y, L) :-
  length([Y|Path], Len),
  reverse([Y|Path], L).
wide_search1([_|T], Len, Y, L) :-
  wide_search1(T, Len, Y, L).
