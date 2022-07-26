# -*- coding: utf-8 -*-
"""
Задание 1.4

Написать тесты для класса CiscoTelnet. Тесты должны проверять:

* создание подключения Telnet при создании экземпляра. Один из признаков
  тут - отсутствие исключений при создании экземлпяра. Также можно
  проверить значение self.prompt
* проверка параметра secret в методе __init__ - при значении по умолчанию None
  (пароль не указывается), надо проверить, что подключение выполнилось без исключений
  и self.prompt равен # или >. Проверить лучше оба значения, так как на оборудовании
  может быть настроен privilege. Если указан правильный пароль secret, проверить что
  получается без ошибок выполнить команды sh clock и sh run | i hostname.
  Плюс self.prompt должен быть равен #
* работу метода send_show_command
* проверить работу экземпляра в менеджере контекста
* приватные методы и переменные мы не проверяем потому что они могут меняться,
  так как это не public API класса и лучше в тестах не привязываться к ним

В целом тут свобода творчества и один из нюансов задания как раз в том чтобы
придумать что именно и как тестировать. В задании даны несколько идей для старта,
но остальное надо продумать самостоятельно.

Тут аналогично 1.3 можно создать отдельный файл с устройствами. В отличии от 1.3,
в этом задании при подключении к оборудованию могут генерироваться исключения,
если что-то пошло не так.
Тест должен проверять, что исключения генерируются и какие именно исключения.

Тест(ы) написать в файле заданий.

Ограничение: класс менять нельзя.
Для заданий этого раздела нет тестов для проверки тестов :)
"""
import time
import telnetlib
import re

import yaml
import pytest


class CiscoTelnet:
    def __init__(
        self,
        host,
        username,
        password,
        secret=None,
        disable_paging=True,
        read_timeout=5,
        encoding="utf-8",
    ):
        self.host = host
        self.username = username
        self.prompt = ">"
        self.read_timeout = read_timeout
        self.encoding = encoding

        self._telnet = telnetlib.Telnet(host)
        self._read_until("Username")
        self._write_line(username)
        self._read_until("Password")
        self._write_line(password)

        match_index, match_obj, output = self._telnet.expect(
            [b">", b"#"], timeout=self.read_timeout
        )
        if not match_obj:
            raise ValueError("Cisco prompt not found")
        self.hostname = re.search(r"(\S+)[#>]", output.decode(self.encoding)).group(1)
        if match_index == 0 and secret:
            self._write_line("enable")
            self._read_until("Password")
            self._write_line(secret)
            if "#" in self._read_until("#"):
                self.prompt = "#"
        elif match_index == 1:
            self.prompt = "#"
        if disable_paging:
            self._write_line("terminal length 0")
            self._read_until(self.prompt)

    def _read_until(self, line):
        output = self._telnet.read_until(
            line.encode(self.encoding), timeout=self.read_timeout
        )
        return output.decode(self.encoding).replace("\r\n", "\n")

    def _write_line(self, line):
        self._telnet.write(f"{line}\n".encode(self.encoding))

    def send_show_command(self, command):
        self._write_line(command)
        command_output = self._read_until(self.prompt)
        return command_output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._telnet.close()


if __name__ == "__main__":
    r1_params = {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with CiscoTelnet(**r1_params) as r1:
        #        print(r1.send_show_command("sh clock"))
        #        print(r1.send_show_command("sh ip int br"))
        print(r1.send_show_command("sh run | i hostname"))


def test_no_route():
    r1_params = {
        "host": "192.168.122.122",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with pytest.raises((OSError)) as exc:
        r1 = CiscoTelnet(**r1_params)


def test_telnet_blocked():
    r1_params = {
        "host": "192.168.122.105",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with pytest.raises((OSError)) as exc:
        r1 = CiscoTelnet(**r1_params)


def test_wrong_password():
    r1_params = {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "123",
        "secret": "cisco",
    }
    with pytest.raises((ValueError)) as exc:
        r1 = CiscoTelnet(**r1_params)


def test_instance():
    r1_params = {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    try:
        r1 = CiscoTelnet(**r1_params)
    except Exception:
        print("Instanse isn't created")
    assert r1.prompt is not None


def test_secret_param(secret_params):
    r1 = CiscoTelnet(**secret_params)
    assert r1.prompt == "#" or r1.prompt == ">"
    if r1.prompt == "#":
        out = r1.send_show_command("sh run | i hostname")
        assert "%" not in out


def test_send_show_command(correct_params):
    out_template = (
        "sh int descr\n"
        "Interface                      Status         Protocol Description\n"
        "Et0/0                          up             up       \n"
        "Et0/1                          admin down     down     \n"
        "Et0/2                          admin down     down     \n"
        "Et0/3                          admin down     down     \n"
        "R1#"
    )
    r1 = CiscoTelnet(**correct_params)
    assert r1.send_show_command("sh int descr") == out_template, "Output doesn't match"


def test_context_manager(correct_params):
    with CiscoTelnet(**correct_params) as r1:
        assert r1.prompt, "There is no prompt"
