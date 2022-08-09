# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать сопрограмму (coroutine) send_config_commands. Сопрограмма
должна подключаться по SSH с помощью asyncssh к одному устройству,
переходить в режим enable, в конфигурационный режим, выполнять указанные команды,
а затем выходить из конфигурационного режима.

Параметры функции:

* host - IP-адрес устройства
* username - имя пользователя
* password - пароль
* enable_password - пароль на режим enable
* config_commands - список команд или одна команда (строка), которые надо выполнить

Функция возвращает строку с результатами выполнения команды:

In [1]: import asyncio

In [2]: from task_17_1 import send_config_commands

In [3]: commands = ['interface loopback55', 'ip address 10.5.5.5 255.255.255.255']

In [4]: print(asyncio.run(send_config_commands('192.168.100.1', 'cisco', 'cisco', 'cisco', commands)))
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface loopback55
R1(config-if)#ip address 10.5.5.5 255.255.255.255
R1(config-if)#end
R1#

In [5]: asyncio.run(send_config_commands(**r1, config_commands=commands))
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loopback55\r\nR1(config-if)#ip address 10.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'


Запустить сопрограмму и проверить, что она работает корректно.
При необходимости можно создавать дополнительные функции.

Для заданий в этом разделе нет тестов!
"""
import asyncio
import asyncssh
from pprint import pprint
import logging

#logging.basicConfig(level="DEBUG")
#asyncssh.set_debug_level(2)

async def custom_read_until(reader, line, timeout=2):
    try:
        return await asyncio.wait_for(reader.readuntil(line), timeout)
    except asyncio.TimeoutError as error:
        output = ""
        while True:
            try:
                output += await asyncio.wait_for(reader.read(1000), 0.1)
            except asyncio.TimeoutError as error:
                break
        print(
            f"TimeoutError при выполнении reader.readuntil('{line}')\n"
            f"Последний вывод:"
        )
        print(output)



async def send_config_commands(
    host, username, password, enable_password, config_commands
):
    if isinstance(config_commands, str):
        config_commands = [config_commands]
    async with await asyncssh.connect(
        host=host,
        username=username,
        password=password,
        known_hosts=None,
        public_key_auth=False,
    ) as ssh:
        writer, reader, stderr = await ssh.open_session(
            term_type="Dumb", term_size=(200, 24)
        )
        await custom_read_until(reader, ">")
        writer.write("enable\n")
        await custom_read_until(reader, "Password")
        writer.write(f"{enable_password}\n")
        await custom_read_until(reader, "#")
        writer.write("terminal length 0\n")
        await custom_read_until(reader, "#")
        writer.write("conf t\n")
        output = await custom_read_until(reader, "#")
        for cmd in config_commands:
            writer.write(f"{cmd}\n")
            output += await custom_read_until(reader, "#")
        writer.write("end\n")
        output += await custom_read_until(reader, "#")
        ssh.close()
    return output


if __name__ == "__main__":

    r1 = {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "enable_password": "cisco",
    }
    config_commands = [
        "int loopback999",
        "ip add 99.99.99.99 255.255.255.255",
        "no shut",
    ]
    pprint(asyncio.run(send_config_commands(**r1, config_commands=config_commands)))
