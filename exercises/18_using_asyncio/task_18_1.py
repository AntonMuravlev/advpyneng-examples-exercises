# -*- coding: utf-8 -*-
"""
Задание 18.1

Создать сопрограмму (coroutine) get_info_network_devices, которая
собирает вывод одной и той же команды со всех устройств в списке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - show команда, которую надо отправить на все устройства

Функция возвращает список с выводом команды с каждого устройства.

In [3]: asyncio.run(get_info_network_devices(devices, command="sh clock"))
Out[3]: ['*14:08:27.584 UTC Wed Sep 12 2021', '*14:08:27.752 UTC Wed Sep 12 2021',
'*14:08:27.755 UTC Wed Sep 12 2021', '*14:08:28.681 UTC Wed Sep 12 2021',
'*14:08:28.879 UTC Wed Sep 12 2021']

Список devices это список словарей в котором могут быть параметры для подключения
к оборудованию с помощюь scrapli и с помощью netmiko (пример в файле devices.yaml).
Функция get_info_network_devices должна распознать как подключаться к устройству -
с помощью scrapli или netmiko по параметру platform/device_type, соответственно.

Функция get_info_network_devices должна подключаться к оборудованию параллельно*
для scrapli - asyncio, а для netmiko - потоки. В идеале подключение в потоках
должно быть сделано так, чтобы оно не блокировало основной поток и другие асинхронные
задачи.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
import asyncio
import yaml
import time
from pprint import pprint
from netmiko import ConnectHandler
from scrapli import AsyncScrapli
from concurrent.futures import ThreadPoolExecutor


async def async_show_command(device, command):
    async with AsyncScrapli(**device) as ssh:
        output = await ssh.send_command(command)
        return output.result, device["host"]


def sync_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        return ssh.send_command(command), device["host"]


async def get_info_network_devices(devices, command):
    executor = ThreadPoolExecutor(max_workers=3)
    tasks = []
    for device in devices:
        if device.get("device_type") == "cisco_ios":
            loop = asyncio.get_running_loop()
            sync_task = loop.run_in_executor(
                executor, sync_show_command, device, command
            )
            print(f"Run sync task {sync_task=}")
            tasks.append(sync_task)
        else:
            async_task = asyncio.create_task(async_show_command(device, command))
            print(f"Run async task {async_task=}")
            tasks.append(async_task)
    results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(get_info_network_devices(devices, command="sh clock"))
    pprint(result)
