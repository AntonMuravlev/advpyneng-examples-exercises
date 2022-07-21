# -*- coding: utf-8 -*-
"""
Задание 4.2c

Скопировать функцию cli и настройку click из задания 4.2a или 4.2b.
Добавить отображение progress bar при выполнении скрипта. Для этого можно
менять функцию send_command_to_devices. При этом функция по-прежнему должна
выполнять подключение в потоках.

Пример вызова:
$ python task_4_2c.py "sh clock" 192.168.100.1 192.168.100.2 192.168.100.3 -u cisco -p cisco -s cisco -t 1
Connecting to devices  [####################################]  100%
['sh clock\r\n*08:35:15.963 UTC Fri Sep 11 2020\r\nR1#',
 'sh clock\r\n*08:35:17.025 UTC Fri Sep 11 2020\r\nR2#',
 'sh clock\r\n*08:35:18.087 UTC Fri Sep 11 2020\r\nR3#']

Для этого задания нет теста!
"""

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
import yaml
import click
from cisco_telnet_class import CiscoTelnet


def send_show_command(device, command):
    with CiscoTelnet(**device) as t:
        output = t.send_show_command(command)
    return output


def send_command_to_devices(devices, command, threads=5):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(send_show_command, device, command) for device in devices
        ]
        with click.progressbar(
            length=len(futures), label="Connecting to devices"
        ) as bar:
            for future in as_completed(futures):
                results.append(future.result())
                bar.update(1)
    return results


# Это просто заготовка, чтобы не забыть, что click надо применять к этой функции
@click.command()
@click.argument("command")
@click.argument("ip_list", nargs=-1, required=True)
@click.option("--username", "-u", prompt=True)
@click.option("--password", "-p", prompt=True, hide_input=True)
@click.option("--secret", "-s", prompt=True, hide_input=True)
@click.option("--threads", "-t", default=5, type=click.IntRange(1, 10))
@click.option("--timed", is_flag=True)
def cli(command, ip_list, username, password, secret, threads, timed):
    devices = [
        {
            "ip": ip,
            "username": username,
            "password": password,
            "enable_password": secret,
        }
        for ip in ip_list
    ]
    if timed:
        start_time = datetime.now()
        pprint(send_command_to_devices(devices, command, threads), width=120)
        delta = datetime.now() - start_time
        print(f"Время выполнения скрипта: {delta}")
    else:
        pprint(send_command_to_devices(devices, command, threads), width=120)


if __name__ == "__main__":
    cli()
