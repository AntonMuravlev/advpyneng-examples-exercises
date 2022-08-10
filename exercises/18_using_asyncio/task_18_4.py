# -*- coding: utf-8 -*-

"""
Задание 18.4

Создать класс CiscoSSH, который наследует класс BaseSSH из файла base_ssh_class.py.

Переписать метод connect в классе CiscoSSH:

1. После подключения по SSH должен выполняться переход в режим enable.
   Для этого также необходимо добавить параметр secret к методу __init__.
2. После перехода в режим enable, отключить paging (команда terminal length 0)

Добавить методы:

* send_show_command - принимает как аргумент команду show и возвращает
  вывод полученный с обрудования
* send_config_commands - должен уметь отправлять одну команду конфигурационного
  режима или список команд. Метод дожен возвращать вывод аналогичный методу
  send_config_set у netmiko.

Проверить работу класса.
Ограничение: нельзя менять класс BaseSSH.

Для заданий в этом разделе нет тестов!
"""
from base_ssh_class import BaseSSH
import asyncio
import asyncssh
import async_timeout


class CiscoSSH(BaseSSH):
    def __init__(self, host, username, password, secret, timeout=30):
        super().__init__(host, username, password, timeout)
        self.secret = secret

    async def _enter_enable(self):
        await self._reader.readuntil(">")
        self._writer.write("enable\n")
        await self._reader.readuntil("Password")
        self._writer.write(f"{self.secret}\n")
        await self._reader.readuntil("#")
        self._writer.write("terminal length 0\n")
        await self._reader.readuntil("#")

    async def connect(self):
        with async_timeout.timeout(self.timeout):
            self._ssh = await asyncssh.connect(
                self.host,
                username=self.username,
                password=self.password,
                known_hosts=None,
                public_key_auth=False,
            )
            self._writer, self._reader, self._stderr = await self._ssh.open_session(
                term_type="Dumb", term_size=(200, 24)
            )
        await self._enter_enable()
        return self

    async def send_show_command(self, command):
        self._writer.write(f"{command}\n")
        output = await self._reader.readuntil("#")
        return output

    async def send_config_commands(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        self._writer.write("conf t\n")
        output = await self._reader.readuntil("#")
        for cmd in commands:
            self._writer.write(f"{cmd}\n")
            output += await self._reader.readuntil("#")
        self._writer.write("end\n")
        output += await self._reader.readuntil("#")
        return output

    def close(self):
        self._ssh.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()


async def main():
    r1_params = {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }

    commands = ["int loop999", "ip add 99.99.99.99 255.255.255.255", "no shut"]
    async with CiscoSSH(**r1_params) as r1:
        print(await r1.send_show_command("show clock"))
        print(await r1.send_config_commands(commands))


if __name__ == "__main__":
    asyncio.run(main())
