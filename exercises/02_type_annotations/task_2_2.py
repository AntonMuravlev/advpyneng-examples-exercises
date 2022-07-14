# -*- coding: utf-8 -*-
"""
Задание 2.2

Написать аннотацию для функций send_show и send_command_to_devices:
аннотация должна описывать параметры и возвращаемое значение.

Проверить код с помощью mypy, если возникли какие-то ошибки, исправить их.

"""

from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from itertools import repeat
import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import SSHException
from typing import Dict, List, Union


def send_show(device_dict: Dict[str, Union[str, int, bool]], command: str) -> str:
    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
        return result
    except SSHException as error:
        return str(error)


def send_command_to_devices(
    devices: List[Dict[str, Union[str, int, bool]]], command: str, max_workers: int = 3
) -> Dict[str, str]:
    data = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        result = executor.map(send_show, devices, repeat(command))
        for device, output in zip(devices, result):
            data[device["host"]] = output
    return reveal_type(data)


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(send_command_to_devices(devices, "sh ip int br"))
