# -*- coding: utf-8 -*-
"""
Задание 1.3

Написать тесты для функции send_show. Тесты должны проверять:

* тип возвращаемых данных - словарь или None, если было исключение
* при возникновении исключения, опционально можно сделать проверку на то правильное ли
  выводится сообщение на stdout, как минимум, что в stdout был вывод IP-адреса
* что функция возвращает правильный результат при передаче команды строки
  и при передаче списка команд. И в том и в том случае должен возвращаться
  словарь в котором ключ команда, а значение вывод команды


Для проверки разных ситуаций - доступное устройство, недоступное и так далее
в файле devices.yaml создано несколько групп устройств:
* reachable_ssh_telnet - это устройства на которых доступен Telnet и SSH, прописаны
  правильные логин и пароли
* reachable_ssh_telnet_wrong_auth_password - это доступное устройство на котором разрешены
  SSH/Telnet, но настроен неправильный пароль auth_password
* reachable_telnet_only - это доступное устройство на котором разрешен только Telnet
  и прописаны правильные логин и пароли
* unreachable - это недоступное устройство

Для корректной работы тестов надо написать в файле devices.yaml параметры ваших устройств
или создать аналогичный файл с другим именем.
Плюс надо соответственно настроить устройства так чтобы где нужно был только
Telnet или неправильный пароль соответственно.

В целом тут свобода творчества и один из нюансов задания как раз в том чтобы
придумать что именно и как тестировать. В задании даны несколько идей для старта,
но остальное надо продумать самостоятельно.

Тест(ы) написать в файле заданий.

Ограничение: функцию менять нельзя.
Для заданий этого раздела нет тестов для проверки тестов :)
"""
import socket
import pytest
from pprint import pprint

import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from paramiko.ssh_exception import SSHException


def send_show(device, show_commands):
    transport = device.get("transport") or "system"
    host = device.get("host")
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    print(f">>> Connecting to {host}")
    try:
        with Scrapli(**device) as ssh:
            for cmd in show_commands:
                reply = ssh.send_command(cmd)
                cmd_dict[cmd] = reply.result
        print(f"<<< Received output from {host}")
        return cmd_dict
    except (ScrapliException, SSHException, socket.timeout, OSError) as error:
        print(f"Device {host}, Transport {transport}, Error {error}")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for dev_type, device_list in devices.items():
            print(dev_type.upper())
        for dev in devices:
            output = send_show(dev, "sh clock")
            pprint(output, width=120)


with open("devices.yaml") as f:
    devices = yaml.safe_load(f)


@pytest.fixture(params=devices)
def device_params(request):
    return request.param


@pytest.fixture()
def input_output():
    one_command = {
        "show ip int br": "Interface                  IP-Address      OK? Method "
        "Status                Protocol\n"
        "Ethernet0/0                192.168.122.101 YES NVRAM  "
        "up                    up\n"
        "Ethernet0/1                unassigned      YES NVRAM  "
        "administratively down down\n"
        "Ethernet0/2                unassigned      YES NVRAM  "
        "administratively down down\n"
        "Ethernet0/3                unassigned      YES NVRAM  "
        "administratively down down"
    }
    commands_list = {
        "show ip int br": "Interface                  IP-Address      OK? Method "
        "Status                Protocol\n"
        "Ethernet0/0                192.168.122.101 YES NVRAM  "
        "up                    up\n"
        "Ethernet0/1                unassigned      YES NVRAM  "
        "administratively down down\n"
        "Ethernet0/2                unassigned      YES NVRAM  "
        "administratively down down\n"
        "Ethernet0/3                unassigned      YES NVRAM  "
        "administratively down down",
        "show int descr": "Interface                      Status         Protocol "
        "Description\n"
        "Et0/0                          up             up\n"
        "Et0/1                          admin down     down\n"
        "Et0/2                          admin down     down\n"
        "Et0/3                          admin down     down",
    }
    return one_command, commands_list


@pytest.fixture()
def first_dev_params():
    return devices[0]


def test_output_type(capsys, device_params):
    output = send_show(device_params, "show clock")
    error_template = (
        f"Device {device_params['host']}, Transport {device_params['transport']}, Error"
    )
    out, err = capsys.readouterr()
    if "Error" in out:
        assert output == None, "Out should be None due exception"
        assert error_template in out, "Error message is wrong"
    else:
        assert isinstance(output, dict), "Out isn't a dict"


def test_output_value(input_output, first_dev_params):
    one_command, commands_list = input_output
    one_command_out = send_show(first_dev_params, list(one_command.keys())[0])
    assert one_command_out == one_command, "One command is sent | Out has a wrong value"
    out_dict = {}
    for command in commands_list.keys():
        out_dict.update(send_show(first_dev_params, command))
    assert (
        commands_list == out_dict
    ), "Multiple commands are sent | Out has a wrong value"
