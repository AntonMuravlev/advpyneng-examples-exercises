# -*- coding: utf-8 -*-
"""
Задание 1.6

Написать тест(ы), который проверяет находятся ли все интерфейсы, которые указаны
в файле net_interfaces_up.yaml в состоянии up (например, столбец Protocol в выводе sh ip int br).

Для проверки надо подключиться к каждому маршрутизатору, который указан
в файле net_interfaces_up.yaml с помощью scrapli/netmiko и проверить статус
интерфейсов. Можно использовать параметры из devices_reachable.yaml.

Тест(ы) должен проходить, если все интерфейсы из файла net_interfaces_up.yaml в состоянии up.
Тест может быть один или несколько. Файл net_interfaces_up.yaml можно менять - писать другие
интерфейсы или IP-адреса, главное чтобы формат оставался таким же.

Тест(ы) написать в файле задания.

Для заданий этого раздела нет тестов для проверки тестов :)
"""


import pytest
import yaml
from pprint import pprint
from scrapli import Scrapli


with open("devices_task5.yaml") as f:
    all_devices = yaml.safe_load(f)

with open("net_interfaces_up.yaml") as f:
    devices_and_intf = yaml.safe_load(f)

ip_list = list(devices_and_intf.keys())

check_devices = []

for device in all_devices:
    if device["host"] in ip_list:
        check_devices.append(device)


@pytest.fixture(scope="session", params=check_devices, ids=ip_list)
def ssh_connection(request):
    ssh = Scrapli(**request.param)
    ssh.open()
    yield ssh
    ssh.close()


def test_ip_intf(ssh_connection):
    intf_list = devices_and_intf[ssh_connection.host]
    parsed_out = ssh_connection.send_command("sh ip int br").textfsm_parse_output()
    real_int_list = [real_int["intf"] for real_int in parsed_out]
    real_int_status = {}
    assert set(intf_list).issubset(set(real_int_list)), "Router doesn't have all interfaces from net_interfaces_up.yaml"
    for real_int in parsed_out:
        real_int_status[real_int["intf"]] = real_int["proto"]
    for intf in intf_list:
        assert real_int_status[intf] == "up"
