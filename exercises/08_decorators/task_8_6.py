# -*- coding: utf-8 -*-
"""
Задание 8.6

Создать декоратор total_order, который добавляет к классу методы:

* __ge__ - операция >=
* __ne__ - операция !=
* __le__ - операция <=
* __gt__ - операция >


Декоратор total_order полагается на то, что в классе уже определены методы:
* __eq__ - операция ==
* __lt__ - операция <

Если методы __eq__ и __lt__ не определены, сгенерировать исключение ValueError при декорации.

Проверить работу декоратора можно на примере класса IPAddress. Класс нельзя менять,
можно только декорировать.
Декоратор не должен использовать переменные класса/экземпляров IPAddress. Для работы методов
должны использоваться только существующие методы __eq__ и __lt__.
Декоратор должен работать и с любым другим классом у которого
есть методы __eq__ и __lt__.


Пример проверки методов с классом IPAddress после декорирования:
In [4]: ip1 = IPAddress('10.10.1.1')

In [5]: ip2 = IPAddress('10.2.1.1')

In [6]: ip1 < ip2
Out[6]: False

In [7]: ip1 > ip2
Out[7]: True

In [8]: ip1 >= ip2
Out[8]: True

In [9]: ip1 <= ip2
Out[9]: False

In [10]: ip1 == ip2
Out[10]: False

In [11]: ip1 != ip2
Out[11]: True

"""
import ipaddress

# def create_ge(eq, lt):
#    return eq
def create_ne(func):
    def wrapper(*args, **kwargs):
        return not func(*args, **kwargs)

    return wrapper


def create_gt(eq_func, lt_func):
    def wrapper(*args, **kwargs):
        def check(*args, **kwargs):
            if not eq_func(*args, **kwargs) and not lt_func(*args, **kwargs):
                return True
            else:
                return False

        return check(*args, **kwargs)

    return wrapper


def create_ge(eq_func, lt_func):
    def wrapper(*args, **kwargs):
        def check(*args, **kwargs):
            if eq_func(*args, **kwargs) or not lt_func(*args, **kwargs):
                return True
            else:
                return False

        return check(*args, **kwargs)

    return wrapper


def create_le(eq_func, lt_func):
    def wrapper(*args, **kwargs):
        def check(*args, **kwargs):
            if eq_func(*args, **kwargs) or lt_func(*args, **kwargs):
                return True
            else:
                return False

        return check(*args, **kwargs)

    return wrapper


def total_order(cls):
    if "__eq__" not in list(vars(cls)):
        raise ValueError("Method __eq__ doesn't exist")
    if "__lt__" not in list(vars(cls)):
        raise ValueError("Method __lt__ doesn't exist")
    setattr(cls, "__ne__", create_ne(cls.__eq__))
    setattr(cls, "__gt__", create_gt(cls.__eq__,cls.__lt__))
    setattr(cls, "__ge__", create_ge(cls.__eq__, cls.__lt__))
    setattr(cls, "__le__", create_le(cls.__eq__, cls.__lt__))
    return cls


@total_order
class IPAddress:
    def __init__(self, ip):
        self._ip = int(ipaddress.ip_address(ip))
        self.ip = ip

    def __repr__(self):
        return f"IPAddress('{self.ip}')"

    def __eq__(self, other):
        return self._ip == other._ip

    def __lt__(self, other):
        return self._ip < other._ip
