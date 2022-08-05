# -*- coding: utf-8 -*-
"""
Задание 14.1

Создать генератор get_ip_from_cfg, который ожидает как аргумент имя файла,
в котором находится конфигурация устройства и возвращает все IP-адреса,
которые настроены на интерфейсах.

Генератор должен обрабатывать конфигурацию и возвращать кортеж на каждой итерации:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например: ('10.0.1.1', '255.255.255.0')

Проверить работу генератора на примере файла config_r1.txt.

"""


def get_ip_from_cfg(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith(" ip address"):
                yield line.split()[2], line.split()[3]


if __name__ == "__main__":
    g1 = get_ip_from_cfg("config_r1.txt")
    for ip_mask in g1:
        print(ip_mask)
