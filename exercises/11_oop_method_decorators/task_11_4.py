# -*- coding: utf-8 -*-
"""
Задание 11.4

Создать класс User, который представляет пользователя.
При создании экземпляра класса, как аргумент передается строка с именем пользователя.

Пример создания экземпляра класса:

In [3]: nata = User('nata')

После этого, должна быть доступна переменная username:
In [4]: nata.username
Out[4]: 'nata'

Переменная username должна быть доступна только для чтения:

In [5]: nata.username = 'user'
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-5-eba76ef1ed86> in <module>
----> 1 nata.username = 'user'

AttributeError: can't set attribute


Также в экземпляре должа быть создана переменная password, но
пока пользователь не установил пароль, при обращении к переменной должно
генерироваться исключение ValueError:

In [6]: nata.password
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-6-7527817bf03d> in <module>
----> 1 nata.password
...
ValueError: Надо установить пароль!

При установке пароля должны выполняться проверки:

* длины пароля - минимальная разрешенная длина пароля 8 символов
* содержится ли имя пользователя в пароле

Если проверки не прошли, надо вывести сообщение об ошибке и запросить пароль еще раз:
(Эта часть задания не тестируется, но ее все равно надо реализовать!)

In [7]: nata.password = 'sadf'
Пароль слишком короткий. Введите пароль еще раз: sdlkjfksnatasdfsd
Пароль содержит имя пользователя. Введите пароль еще раз: asdfkpeorti2435
Пароль установлен

Если пароль прошел проверки, должно выводиться сообщение "Пароль установлен"

In [8]: nata.password = 'sadfsadfsadf'
Пароль установлен
"""


class User:
    def __init__(self, username):
        self._username = username
        self._password = None

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        if not self._password:
            raise ValueError("Надо установить пароль!")
        return self._password

    @password.setter
    def password(self, new_pass):
        check_flag = True
        while check_flag:
            if len(new_pass) < 8:
                new_pass = input("Пароль слишком короткий. Введите пароль еще раз: ")
            elif self._username in new_pass:
                new_pass = input(
                    "Пароль содержит имя пользователя. Введите пароль еще раз:"
                )
            else:
                self._password = new_pass
                print("Пароль установлен")
                check_flag = False
