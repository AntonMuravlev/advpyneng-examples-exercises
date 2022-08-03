# -*- coding: utf-8 -*-
"""
Задание 12.2

Скопировать класс IPv4Network из задания 11.1 и изменить его таким
образом, чтобы класс IPv4Network наследовал абстрактный класс Sequence из collections.abc.
Создать все необходимые абстрактные методы для работы IPv4Network как Sequence.

Проверить, что работают все методы характерные для последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__, index, count

Пример создания экземпляра класса:

In [1]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [2]: len(net1)
Out[2]: 6

In [3]: net1[0]
Out[3]: '8.8.4.1'

In [4]: '8.8.4.1' in net1
Out[4]: True

In [5]: '8.8.4.10' in net1
Out[5]: False

In [6]: net1.count('8.8.4.1')
Out[6]: 1

In [7]: net1.index('8.8.4.1')
Out[7]: 0

In [8]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6


"""
import ipaddress
from collections.abc import Sequence


class IPv4Network(Sequence):
    def __init__(self, network, gw=None):
        self._net = ipaddress.ip_network(network)
        self.network = network
        self.broadcast = str(self._net.broadcast_address)
        self.gw = gw
        self._hosts = self.hosts
        self.allocated = set()
        self.unassigned = set(self.hosts)
        if self.gw:
            self.allocated.add(self.gw)
            self.unassigned.remove(self.gw)

    def __getitem__(self, item):
        return self.hosts[item]

    def __len__(self):
        return len(self.hosts)

    @property
    def hosts(self):
        return tuple([str(h) for h in self._net.hosts()])

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
    net = IPv4Network("100.7.1.0/29")
    print(f"{net[0]=}")
    print(f"{len(net)=}")
    print(f"{'100.7.1.2' in net=}")
    print(f"{iter(net)=}")
    print(f"{net.index('100.7.1.3')=}")
    print(f"{net.count('100.7.1.2')=}")
