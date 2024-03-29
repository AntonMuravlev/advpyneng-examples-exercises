# -*- coding: utf-8 -*-
"""
Задание 13.4

Скопировать и переделать класс IPv4Network из задания 9.1
с использованием dataclass. У каждого экземпляра класса
IPv4Network должны быть такие переменные:

* network - строка вида "10.1.1.0/29"
* broadcast - строка вида "10.1.1.7"
* gw - None или строка вида "10.1.1.1"
* hosts - кортеж со всеми IP-адресами указанной сети
  пример для net1 ('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6')
* allocated - множество IP-адресов, которые назначены на какие-то устройства в сети
* unassigned - множество со свободными IP-адресами

И такие методы:

* allocate_ip - ожидает как аргумент один IP-адрес. Если адрес входит в сеть экземпляра
  и еще не выделен, метод добавляет адрес в множество allocated (и удаляет из unassigned).
  Если адрес не из сети экземпляра, генерируется исключение ValueError. Если адрес уже
  находится в allocated, генерируется ValueError.
* free_ip - делает обратную операцию по сравнению с allocate_ip, аналогично работает с
  множествами allocated и unassigned. И генерирует ValueError при попытке освободить адрес,
  который и так свободен

Для реализации функционала класса можно использовать модуль ipaddress.

Пример создания экземпляра класса:

In [1]: from task_13_4 import IPv4Network

In [2]: net1 = IPv4Network('10.1.1.0/29')

In [3]: net1
Out[3]: IPv4Network(network='10.1.1.0/29', hosts=('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6'))

In [4]: net1.network
Out[4]: '10.1.1.0/29'

In [5]: net1.broadcast
Out[5]: '10.1.1.7'

In [6]: net1.gw

In [7]: net1.allocated
Out[7]: set()

In [8]: net1.unassigned
Out[8]: {'10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6'}

In [9]: net1.hosts
Out[9]: ('10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4', '10.1.1.5', '10.1.1.6')

In [10]: net1 = IPv4Network('10.1.1.0/29', gw='10.1.1.1')

In [11]: net1.allocated
Out[11]: {'10.1.1.1'}

In [12]: net1.allocate_ip('10.1.1.3')

In [13]: net1.allocate_ip('10.1.1.6')

In [14]: net1.allocated
Out[14]: {'10.1.1.1', '10.1.1.3', '10.1.1.6'}

In [15]: net1.unassigned
Out[15]: {'10.1.1.2', '10.1.1.4', '10.1.1.5'}

"""
from dataclasses import dataclass, field
import ipaddress


@dataclass
class IPv4Network:
    network: str
    broadcast: str = field(init=False)
    gw: str = None
    hosts: tuple = field(init=False)
    allocated: set = field(default_factory=set)
    unassigned: set = field(init=False)

    def __post_init__(self):
        _net = ipaddress.ip_network(self.network)
        self.broadcast = str(_net.broadcast_address)
        self.hosts = tuple(str(h) for h in _net.hosts())
        self.unassigned = set(self.hosts)
        if self.gw:
            self.allocated.add(self.gw)
            self.unassigned.remove(self.gw)

    def allocate_ip(self, ip):
        if ip in self.hosts and ip not in self.allocated:
            self.allocated.add(ip)
            self.unassigned.remove(ip)
        else:
            raise ValueError

    def free_ip(self, ip):
        if ip in self.hosts and ip in self.allocated:
            self.allocated.remove(ip)
            self.unassigned.add(ip)
        else:
            raise ValueError


if __name__ == "__main__":
    # Примеры обращения к переменным и вызова методов
    net1 = IPv4Network("10.1.1.0/29")
    # net1 = IPv4Network('10.1.1.0/29', gw="10.1.1.1")
    print(f"{net1.broadcast=}")
    print(f"{net1.hosts=}")
    print(f"{net1.allocated=}")
    print(f"{net1.unassigned=}")

    # allocate ip:
    print(f">>> {net1.allocate_ip('10.1.1.6')=}")
    print(f">>> {net1.allocate_ip('10.1.1.3')=}")
    print(f"{net1.allocated=}")
    print(f"{net1.unassigned=}")
    print(f"<<< {net1.free_ip('10.1.1.3')=}")
    print(f"{net1.allocated=}")
    print(f"{net1.unassigned=}")
    print(f">>> {net1.allocate_ip('10.1.1.3')=}")
    # print(f">>> {net1.allocate_ip('10.1.1.3')=}") # ValueError
    # print(f">>> {net1.allocate_ip('10.1.1.113')=}") # ValueError
    print(f"{net1.allocated=}")
    print(f"{net1.unassigned=}")
