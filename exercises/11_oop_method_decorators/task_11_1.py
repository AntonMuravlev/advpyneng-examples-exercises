# -*- coding: utf-8 -*-
"""
Задание 11.1

Скопировать класс IPv4Network из задания 9.1.
Переделать класс таким образом, чтобы запись значения в переменную hosts
была запрещена.


Пример создания экземпляра класса:
In [1]: net1 = IPv4Network('8.8.4.0/29')

In [2]: net1.hosts
Out[2]: ('8.8.4.1', '8.8.4.2', '8.8.4.3', '8.8.4.4', '8.8.4.5', '8.8.4.6')

Запись переменной:

In [6]: net1.hosts = 'test'
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-6-c98e898835e1> in <module>
----> 1 net1.hosts = 'test'

AttributeError: can't set attribute

"""
import ipaddress

class IPv4Network:
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

