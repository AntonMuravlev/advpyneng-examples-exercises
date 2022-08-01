# -*- coding: utf-8 -*-
"""
Задание 10.2

Скопировать класс PingNetwork из задания 9.2 и изменить его таким образом,
чтобы адреса пинговались не при вызове метода scan, а при вызове экземпляра.

Вся функциональность метода scan должна быть перенесена в метод, который отвечает
за вызов экземпляра.

Пример работы с классом PingNetwork. Сначала создаем сеть:
In [2]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [3]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

Затем создается экземпляр класса PingNetwork, сеть передается как аргумент:
In [6]: ping_net = PingNetwork(net1)

После этого экземпляр должен быть вызываемым объектом (callable):

In [7]: ping_net()
Out[7]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [8]: ping_net(include_unassigned=True)
Out[8]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])

"""
import subprocess
from task_10_1 import IPv4Network
from concurrent.futures import ThreadPoolExecutor


class PingNetwork:
    def __init__(self, net):
        self.net = net

    def _ping(self, ip):
        result = subprocess.run(
            [(f"ping {ip} -i 0.2 -c 3 -n -W 1")], shell=True, stdout=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return True
        else:
            return False

    def __call__(self, workers=5, include_unassigned=False):
        reach_ip = []
        unreach_ip = []
        all_ip = self.net.allocated
        if include_unassigned:
            all_ip = self.net.hosts
        with ThreadPoolExecutor(max_workers=workers) as executor:
            result = executor.map(self._ping, all_ip)
            for r, ip in zip(result, all_ip):
                if r:
                    reach_ip.append(ip)
                else:
                    unreach_ip.append(ip)
        return (reach_ip, unreach_ip)


if __name__ == "__main__":
    net1 = IPv4Network("8.8.4.0/29")
    net1.allocate_ip("8.8.4.2")
    net1.allocate_ip("8.8.4.4")
    net1.allocate_ip("8.8.4.6")

    ping_net = PingNetwork(net1)
    print(ping_net())
