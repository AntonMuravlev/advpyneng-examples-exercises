# -*- coding: utf-8 -*-
"""
Задание 17.5

Создать сопрограмму (coroutine) configure_net_devices.

Параметры configure_net_devices:
* devices - список словарей с параметрами подключения к устройствам
* device_commands_map - словарь в котором указано на какое устройство
  отправлять какие команды. Пример словаря - host_commands_dict

Функция возвращает словарь:

* ключ - IP-адрес устройства с которого получен вывод
* значение - вывод, который вернула функция configure_router для этого устройства или
  исключение

Сопрограмма configure_net_devices должна настраивать оборудование в соответствии
со словарем device_commands_map - отправлять команды в значении на то оборудование,
которое указано в ключе словаря. Оборудование должно настраиваться параллельно*.
Для непосредственной настройки оборудования, надо использовать функцию
configure_router из задания 17.4.

Между словарем device_commands_map и списком словарей devices (параметры функции)
может быть несоответствие. Например, в словаре device_commands_map могут быть
устройства для которых не указаны параметры подключения в списке devices. И наоборот.
Функция configure_net_devices должна отправлять команды только на те устройства
для которых есть словарь с параметрами подключения в списке devices и команды
в словаре device_commands_map.

Пример команд и словаря для проверки настройки есть в задании.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""


import asyncio
from pprint import pprint
import yaml
from task_17_4 import configure_router


async def configure_net_devices(devices, device_commands_map):
    hosts = host_commands_dict.keys()
    actual_devices = [device for device in devices if device["host"] in hosts]
    actual_hosts = [device["host"] for device in actual_devices]
    coroutines = (
        configure_router(device, device_commands_map[device["host"]])
        for device in actual_devices
    )
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    out_dict = dict(zip(actual_hosts, results))
    return out_dict


if __name__ == "__main__":
    ospf = [
        "router ospf 55",
        "auto-cost reference-bandwidth 1000000",
        "network 0.0.0.0 255.255.255.255 area 0",
    ]
    logging_with_error = "logging 0255.255.1"
    logging_correct = "logging buffered 20010"

    host_commands_dict = {
        "192.168.122.102": logging_correct,
        "192.168.122.103": logging_with_error,
        "192.168.122.101": ospf,
    }
    with open("devices_scrapli.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(asyncio.run(configure_net_devices(devices, host_commands_dict)))
