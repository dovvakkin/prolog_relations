# prolog_relations
Family relations database in prolog with pythonic CLI

Данный проект -- база данных о родственных связях на прологе и интерфейс командной строки на питоне к ней.
Интерфейс поддерживает следующие типы запросов:
* В каком родстве состоят `$имя1` и `$имя2`
* Кто `$родственное_отношение` `$имя`
* Чей `$родственное_отношение` `$имя`
* Добавление новых родственных отношений

Формат запросов произвольный (то есть корректными запросами являются _кто муж Алисы_ и _кому Алиса приходится женой_)

Для добавления новых отношений к отношению в произвольном формате следует добавить префикс `ДОБАВИТЬ` (например, _ДОБАВИТЬ Ольга дочь Сергея_)

В вопросах про степень родства итоговое родство строится как композиция родственных связей, причём кратчайшая такая композиция (например, _Анна -- дочь Владимира, внука Ивана_)

---------
Следует иметь в виду, что некоторые незначительные ошибки, появляющиеся при добавлении новых имён, скорее всего, вызваны ошибками при нормализации в `pymorphy`
