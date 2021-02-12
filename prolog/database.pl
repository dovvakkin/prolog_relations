:- dynamic мужчина/1.
:- dynamic женщина/1.
:- dynamic родитель/2.
:- dynamic супруг1/2.

мужчина('Иван').
мужчина('Федор').
мужчина('Сергей').
мужчина('Александр').
мужчина('Владимир').
мужчина('Альберт').
мужчина('Максим').
мужчина('Егор').
мужчина('Петр').
мужчина('Андрей').

женщина('Анастасия').
женщина('Анна').
женщина('Екатерина').
женщина('Мария').
женщина('Алиса').
женщина('Алёна').
женщина('Ирина').
женщина('Софья').
женщина('Ольга').
женщина('Елена').

супруг(X, Y) :- супруг1(Y, X); супруг1(X, Y).
супруг1('Иван', 'Анастасия').
супруг1('Александр', 'Софья').
супруг1('Сергей', 'Алиса').
супруг1('Владимир', 'Алёна').
супруг1('Екатерина', 'Федор').

родитель('Иван', 'Федор').
родитель('Иван', 'Сергей').
родитель('Анастасия', 'Федор').
родитель('Анастасия', 'Сергей').
родитель('Александр', 'Алиса').
родитель('Александр', 'Егор').
родитель('Софья', 'Алиса').
родитель('Софья', 'Егор').
родитель('Федор', 'Максим').
родитель('Федор', 'Владимир').
родитель('Екатерина', 'Максим').
родитель('Екатерина', 'Владимир').
родитель('Сергей', 'Мария').
родитель('Алиса', 'Мария').
родитель('Владимир', 'Альберт').
родитель('Владимир', 'Ирина').
родитель('Владимир', 'Анна').
родитель('Алёна', 'Альберт').
родитель('Алёна', 'Ирина').
родитель('Алёна', 'Анна').