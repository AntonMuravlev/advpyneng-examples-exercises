# -*- coding: utf-8 -*-
"""
Задание 10.1

Скопировать класс IPv4Network из задания 9.1 и добавить ему все методы,
которые необходимы для реализации протокола последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__
* index, count - должны работать аналогично методам в списках и кортежах

И оба метода, которые отвечают за строковое представление экземпляров
класса IPv4Network.

Существующие методы и атрибуты (из задания 9.1) можно менять, при необходимости.

Пример создания экземпляра класса:

In [2]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [3]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6

In [4]: net1[2]
Out[4]: '8.8.4.3'

In [5]: net1[-1]
Out[5]: '8.8.4.6'

In [6]: net1[1:4]
Out[6]: ('8.8.4.2', '8.8.4.3', '8.8.4.4')

In [7]: '8.8.4.4' in net1
Out[7]: True

In [8]: net1.index('8.8.4.4')
Out[8]: 3

In [9]: net1.count('8.8.4.4')
Out[9]: 1

In [10]: len(net1)
Out[10]: 6

Строковое представление:

In [13]: net1
Out[13]: IPv4Network(8.8.4.0/29)

In [14]: str(net1)
Out[14]: 'IPv4Network 8.8.4.0/29'

"""
import ipaddress


class IPv4Network:
    def __init__(self, network, gw=None):
        _net = ipaddress.ip_network(network)

        self.network = network
        self.broadcast = str(_net.broadcast_address)
        self.gw = gw
        self.hosts = tuple([str(h) for h in _net.hosts()])
        self.allocated = set()
        self.unassigned = set(self.hosts)
        if self.gw:
            self.allocated.add(self.gw)
            self.unassigned.remove(self.gw)

    def __str__(self):
        return f"IPv4Network {self.network}"

    def __repr__(self):
        return f"IPv4Network({self.network})"

    def __getitem__(self, item):
        return self.hosts[item]

    def __len__(self):
        return len(self.hosts)

    def __contains__(self, value):
        return True if value in self.hosts else False

    def __iter__(self):
        return iter(self.hosts)

    def count(self, value):
        return self.hosts.count(value)

    def index(self, value):
        return self.hosts.index(value)

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
