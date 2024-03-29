# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать класс Topology, который представляет топологию сети.
Класс Topology должен наследовать абстрактный класс MutableMapping
и для всех абстрактных методов класса MutableMapping должна быть
написана рабочая реализация в классе Topology.

Проверить, что после реализации абстрактных методов, работают также
такие методы: keys, items, values, get, pop, popitem, clear, update, setdefault.

При создании экземпляра класса, как аргумент передается словарь, который описывает топологию.
В каждом экземпляре должна быть создана переменная topology, в которой
содержится словарь топологии.

Пример создания экземпляра класса:
In [1]: t1 = Topology(example1)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка реализации абстрактных методов:

получение элемента:
In [3]: t1[('R1', 'Eth0/0')]
Out[3]: ('SW1', 'Eth0/1')


Перезапись/добавление элемента:
In [5]: t1[('R1', 'Eth0/0')] = ('SW1', 'Eth0/12')

In [6]: t1.topology
Out[6]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [7]: t1[('R6', 'Eth0/0')] = ('SW1', 'Eth0/17')

In [8]: t1.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R6', 'Eth0/0'): ('SW1', 'Eth0/17')}


Удаление:
In [11]: del t1[('R6', 'Eth0/0')]

In [12]: t1.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/12'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Итерация:
In [13]: for item in t1:
    ...:     print(item)
    ...:
('R1', 'Eth0/0')
('R2', 'Eth0/0')
('R2', 'Eth0/1')
('R3', 'Eth0/0')
('R3', 'Eth0/1')
('R3', 'Eth0/2')

Длина:
In [14]: len(t1)
Out[14]: 6

После реализации абстрактных методов, должны работать таким методы:

In [1]: t1.topology
Out[1]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

keys, values, items:
In [2]: t1.keys()
Out[2]: KeysView(<__main__.Topology object at 0xb562f82c>)

In [3]: t1.values()
Out[3]: ValuesView(<__main__.Topology object at 0xb562f82c>)

Метод get:
In [4]: t1.get(('R2', 'Eth0/0'))
Out[4]: ('SW1', 'Eth0/2')

In [6]: print(t1.get(('R2', 'Eth0/4')))
None

Метод pop:
In [8]: t1.pop(('R2', 'Eth0/0'))
Out[8]: ('SW1', 'Eth0/2')

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Метод update:
In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [11]: t1.update(t2)

In [13]: t1.topology
Out[13]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Метод clear:
In [14]: t1.clear()

In [15]: t1.topology
Out[15]: {}

"""
from typing import Dict, List, Tuple
from collections.abc import MutableMapping
from pprint import pprint


class Topology(MutableMapping):
    def __init__(self, topology_dict: Dict[Tuple[str, str], Tuple[str, str]]) -> None:
        self.topology = self._normalize(topology_dict)

    @staticmethod
    def _normalize(
        topology_dict: Dict[Tuple[str, str], Tuple[str, str]]
    ) -> Dict[Tuple[str, str], Tuple[str, str]]:
        normalized_topology = {}
        for box, neighbor in topology_dict.items():
            if not neighbor in normalized_topology:
                normalized_topology[box] = neighbor
        return normalized_topology

    def __getitem__(self, item):
        return self.topology[item]

    def __setitem__(self, key, value):
        self.topology[key] = value

    def __delitem__(self, key):
        del self.topology[key]

    def __iter__(self):
        return iter(self.topology)

    def __len__(self):
        return len(self.topology)


if __name__ == "__main__":
    example1 = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R4", "Eth0/0"): ("R3", "Eth0/1"),
        ("R5", "Eth0/0"): ("R3", "Eth0/2"),
    }

    example2 = {("R1", "Eth0/4"): ("R7", "Eth0/0"), ("R1", "Eth0/6"): ("R9", "Eth0/0")}
    t1 = Topology(example1)

    pprint(f"{t1.topology=}")
    pprint(f"{t1[('R1', 'Eth0/0')]=}")
    t1[("R1", "Eth0/0")] = ("SW1", "Eth0/12")
    pprint(f"{t1.topology}")
    t1[("R6", "Eth0/0")] = ("SW1", "Eth0/17")
    pprint(f"{t1.topology}")
    del t1[("R6", "Eth0/0")]
    pprint(f"{t1.topology}")
    pprint(f"{iter(t1)=}")
    pprint(f"{t1.keys()=}")
    pprint(f"{t1.values()=}")
    pprint(f"{t1.items()=}")
    pprint(f"{t1.get(('R2', 'Eth0/0'))=}")
    pprint(f"{t1.pop(('R2', 'Eth0/0'))=}")
    t2 = Topology(example2)
    pprint(f"{t2.topology=}")
    t1.update(t2)
    pprint(f"{t1.topology}")
