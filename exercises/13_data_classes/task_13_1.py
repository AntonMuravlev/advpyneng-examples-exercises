# -*- coding: utf-8 -*-
"""
Задание 13.1

Создать класс Route с использованием dataclass. У экземпляров класса должны быть
доступны переменные: prefix, nexthop и protocol.
В строковом представлении экземпляров не должна выводиться информация о протоколе.

Пример создания экземпляра класса:

In [2]: route1 = Route('10.1.1.0/24', '10.2.2.2', 'OSPF')

После этого, должны быть доступны переменные prefix, nexthop и protocol:

In [3]: route1.nexthop
Out[3]: '10.2.2.2'

In [4]: route1.prefix
Out[4]: '10.1.1.0/24'

In [5]: route1.protocol
Out[5]: 'OSPF'


Строковое представление:

In [6]: route1
Out[6]: Route(prefix='10.1.1.0/24', nexthop='10.2.2.2')
"""

from dataclasses import dataclass, field


@dataclass
class Route:
    prefix: str
    nexthop: str
    protocol: str = field(repr=False)


if __name__ == "__main__":
    route1 = Route("10.1.1.0/24", "10.2.2.2", "OSPF")
    print(route1)
