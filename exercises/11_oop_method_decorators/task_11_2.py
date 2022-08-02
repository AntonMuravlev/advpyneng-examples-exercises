# -*- coding: utf-8 -*-
"""
Задание 11.2

Скопировать класс PingNetwork из задания 9.2.
Один из методов класса зависит только от значения аргумента и не зависит
от значений переменных экземпляра или другого состояния объекта.

Сделать этот метод статическим и проверить работу метода.

"""
import subprocess
from task_11_1 import IPv4Network
from concurrent.futures import ThreadPoolExecutor


class PingNetwork:
    def __init__(self, net):
        self.net = net

    @staticmethod
    def _ping(ip):
        result = subprocess.run(
            [(f"ping {ip} -i 0.2 -c 3 -n -W 1")], shell=True, stdout=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return True
        else:
            return False

    def scan(self, workers=5, include_unassigned=False):
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
    print(ping_net.scan())
