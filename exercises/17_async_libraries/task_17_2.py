# -*- coding: utf-8 -*-
"""
Задание 17.2

Создать сопрограмму (coroutine) configure_devices. Сопрограмма
должна настраивать одни и те же команды на указанных устройствах с помощью asyncssh.
Все устройства должны настраиваться параллельно.

Параметры функции:

* devices - список словарей с параметрами подключения к устройствам
* config_commands - команды конфигурационного режима, которые нужно отправить на каждое устройство

Функция возвращает список строк с результатами выполнения команды на каждом устройстве.
Запустить сопрограмму и проверить, что она работает корректно с устройствами
в файле devices.yaml и командами в списке commands.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
import asyncio
import asyncssh
import yaml
from pprint import pprint
from task_17_1 import send_config_commands


async def configure_devices(devices, config_commands):
    coroutines = [
        send_config_commands(**device, config_commands=config_commands)
        for device in devices
    ]
    result = await asyncio.gather(*coroutines)
    out_dict = {device["host"]: out
            for device in devices
            for out in result}
    return out_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    config_commands = [
        "int loopback999",
        "ip add 99.99.99.99 255.255.255.255",
        "no shut",
    ]
    pprint(asyncio.run(configure_devices(devices, config_commands)))
