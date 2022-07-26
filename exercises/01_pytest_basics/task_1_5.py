# -*- coding: utf-8 -*-
"""
Задание 1.5

Написать тест(ы), который проверяет есть ли маршрут 192.168.100.0/24 в таблице
маршрутизации (команда sh ip route) на маршрутизаторах, которые указаны в файле devices_reachable.yaml.

Для проверки надо подключиться к каждому маршрутизатору с помощью scrapli
и проверить маршрут командой sh ip route или разновидностью команды sh ip route.

Тест(ы) должен проходить, если маршрут есть.
Тест может быть один или несколько.

Тест(ы) написать в файле задания.

Для заданий этого раздела нет тестов для проверки тестов :)
"""


import pytest
import yaml
from pprint import pprint
from scrapli import Scrapli


with open("devices_task5.yaml") as f:
    devices = yaml.safe_load(f)
ip_list = [device["host"] for device in devices]


@pytest.fixture(scope="session", params=devices, ids=ip_list)
def ssh_connection(request):
    ssh = Scrapli(**request.param)
    ssh.open()
    yield ssh
    ssh.close()


def test_route_table(ssh_connection):
    reply = ssh_connection.send_command("sh ip route 192.168.122.0 255.255.255.0")
    assert "% Network not in table" not in reply.result
