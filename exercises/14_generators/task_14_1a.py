# -*- coding: utf-8 -*-
"""
Задание 14.1a

Создать генератор get_intf_ip, который ожидает как аргумент имя файла,
в котором находится конфигурация устройства и возвращает все интерфейсы и IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать кортеж на каждой итерации:
* первый элемент кортежа - имя интерфейса
* второй элемент кортежа - IP-адрес
* третий элемент кортежа - маска

Например: ('FastEthernet', '10.0.1.1', '255.255.255.0')

Проверить работу генератора на примере файла config_r1.txt.
"""


def get_intf_ip(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith("interface"):
                intf = line.split()[1]
            if line.startswith(" ip address"):
                yield intf, line.split()[2], line.split()[3]


if __name__ == "__main__":
    g1 = get_intf_ip("config_r1.txt")
    for intf in g1:
        print(intf)
