# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать сопрограмму (coroutine) config_device_and_check. Сопрограмма
должна подключаться по SSH с помощью scrapli к одному устройству,
переходить в режим enable, в конфигурационный режим, выполнять указанные команды,
а затем выходить из конфигурационного режима. После  настройки команд, функция
должна проверять, что они настроены корректно. Для проверки используется словарь (пояснение ниже).
Если проверка не прошла, должно генерироваться исключение ValueError с текстом на каком
устройстве не прошла проверка. Если проверка прошла, функция должна возвращать строку
с результатами выполнения команды.

Параметры функции:

* device - словарь с параметрами подключения к устройству
* config_commands - список команд или одна команда (строка), которые надо выполнить
* check - словарь, который указывает как проверить настройку команд config_commands. По умолчанию значение None.

Словарь, который передается в параметр check должен содержать две пары ключ-значение:
* command - команда, которая используется для проверки конфигурации
* search_line - какая строка должна присутствовать в выводе команды command

Запустить сопрограмму и проверить, что она работает корректно одним из устройств
в файле devices_scrapli.yaml и командами в списке commands.
Пример команд и словаря для проверки настройки есть в задании.

При необходимости, можно использовать функции из предыдущих заданий
и создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
import yaml
import asyncio
from scrapli import AsyncScrapli
import logging

#logging.basicConfig(level="DEBUG")
#asyncssh.set_debug_level(2)


async def config_device_and_check(device, config_commands, check=None):
    async with AsyncScrapli(**device) as ssh:
        if isinstance(config_commands, str):
            config_commands = [config_commands]
        await ssh.send_configs(config_commands)
        output = await ssh.send_command(check["command"])
        if check["search_line"] not in output.result:
            raise ValueError(f"Validaition is failed on {device['host']}")
        return output.result


if __name__ == "__main__":
    commands = [
        "router ospf 55",
        "auto-cost reference-bandwidth 1000000",
        "network 0.0.0.0 255.255.255.255 area 0",
    ]

    check_ospf = {
        "command": "sh ip ospf",
        "search_line": 'Routing Process "ospf 55" with ID',
    }

    with open("devices_scrapli.yaml") as f:
        devices = yaml.safe_load(f)

    print(asyncio.run(config_device_and_check(devices[1], commands, check_ospf)))
