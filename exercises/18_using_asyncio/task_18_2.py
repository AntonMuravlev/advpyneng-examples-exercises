# -*- coding: utf-8 -*-
"""
Задание 18.2

Создать сопрограмму (coroutine) ping_ip_addresses, которая проверяет
пингуются ли IP-адреса в списке.
Проверка IP-адресов должна выполняться параллельно (concurrent).

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:

* список доступных IP-адресов
* список недоступных IP-адресов


Для проверки доступности IP-адреса, используйте утилиту ping встроенную в ОС.

Запустить сопрограмму и проверить, что она работает корректно.
При необходимости можно создавать дополнительные функции.

Для заданий в этом разделе нет тестов!

"""

import asyncio


async def ping(ip):
    reply = await asyncio.create_subprocess_shell(
        f"ping -c 2 -W 0.1 {ip}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await reply.communicate()
    if reply.returncode == 0:
        return True, ip
    else:
        return False, ip


async def ping_ip_list(ip_list):
    coroutines = [ping(ip) for ip in ip_list]
    results = await asyncio.gather(*coroutines)
    reach = [result[1] for result in results if result[0]]
    unreach = [result[1] for result in results if not result[0]]
    return reach, unreach


if __name__ == "__main__":
    ip_list = ["192.168.122.101", "192.168.122.102", "192.168.100.3", "192.168.122.1"]
    output = asyncio.run(ping_ip_list(ip_list))
    print(output)
