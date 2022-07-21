# -*- coding: utf-8 -*-
"""
Задание 4.3

Создать интерфейс командной строки для скрипта по выводу help ниже.

Help скрипта:

$ python task_4_3.py --help
Usage: task_4_3.py [OPTIONS] COMMAND [ARGS]...

  Скрипт работает с устройствами в файле YAML_PARAMS и выполняет операции в
  потоках THREADS

Options:
  -y, --yaml-params FILENAME   [default: devices_task_4_3.yaml]
  -t, --threads INTEGER RANGE  [default: 5]
  --help                       Show this message and exit.

Commands:
  config  Отправить конфигурационные команды из файла COMMANDS
  ping    Пинг устройств из файла YAML_PARAMS
  show    Отправить show COMMAND и опционально парсить (PARSE) ее с помощью...

Help команд:

$ python task_4_3.py config --help
Usage: task_4_3.py config [OPTIONS] COMMANDS

  Отправить конфигурационные команды из файла COMMANDS

Options:
  --help  Show this message and exit.


$ python task_4_3.py ping --help
Usage: task_4_3.py ping [OPTIONS]

  Пинг устройств из файла YAML_PARAMS

Options:
  --help  Show this message and exit.


$ python task_4_3.py show --help
Usage: task_4_3.py show [OPTIONS] COMMAND

  Отправить show COMMAND и опционально парсить (PARSE) ее с помощью textfsm
  и/или записать результат в OUTPUT_FILE

Options:
  -o, --output-file FILENAME  Записать результат в файл
  -p, --parse                 Парсить вывод с помощью textfsm
  --help                      Show this message and exit.



Примеры использования скрипта (вывод сокращен):

Команда config отправляет команды из файла, который передается как аргумент на все указанные устройства:

$ python task_4_3.py -y devices_task_4_3.yaml config config_commands.txt
{'192.168.100.1': 'configure terminal\n'
                  'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                  'R1(config)#interface Loopback99\n'
                  'R1(config-if)#ip address 10.0.99.1 255.255.255.0\n'
                  'R1(config-if)#end\n'
                  'R1#',
 '192.168.100.2': 'configure terminal\n'
                  'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                  'R2(config)#interface Loopback99\n'
                  'R2(config-if)#ip address 10.0.99.1 255.255.255.0\n'
                  'R2(config-if)#end\n'
                  'R2#',
 '192.168.100.3': 'configure terminal\n'
                  'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                  'R3(config)#interface Loopback99\n'
                  'R3(config-if)#ip address 10.0.99.1 255.255.255.0\n'
                  'R3(config-if)#end\n'
                  'R3#'}

Команда ping пингует устройства из файла -y devices_task_4_3.yaml:

$ python task_4_3.py -y devices_task_4_3.yaml ping
Доступные адреса:   192.168.100.1, 192.168.100.2, 192.168.100.3
Недоступные адреса:

Команда show отправляет указанную команду show на все указанные устройства из файла -y devices_task_4_3.yaml и выводит результат:

$ python task_4_3.py -y devices_task_4_3.yaml show "sh clock"
{'192.168.100.1': '*09:22:19.639 UTC Mon Sep 21 2020',
 '192.168.100.2': '*09:22:19.656 UTC Mon Sep 21 2020',
 '192.168.100.3': '*09:22:19.783 UTC Mon Sep 21 2020'}

С опцией -p вывод команд парсится с помощью textfsm и выводится:

$ python task_4_3.py -y devices_task_4_3.yaml show "sh ip int br" -p
{'192.168.100.1': [{'interface': 'FastEthernet0/0',
                    'ip': '192.168.100.1',
                    'protocol': 'up',
                    'status': 'up'},
                   {'interface': 'Loopback99',
                    'ip': '10.0.99.1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'interface': 'FastEthernet0/0',
                    'ip': '192.168.100.2',
                    'protocol': 'up',
                    'status': 'up'},
                   {'interface': 'Loopback99',
                    'ip': '10.0.99.1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.3': [{'interface': 'FastEthernet0/0',
                    'ip': '192.168.100.3',
                    'protocol': 'up',
                    'status': 'up'},
                   {'interface': 'Loopback99',
                    'ip': '10.0.99.1',
                    'protocol': 'up',
                    'status': 'up'}]}

Опция -o добавляет запись результата в файл (примеры файлов с записью данных выложены в каталоге 04_click):

$ python task_4_3.py -y devices_task_4_3.yaml show "sh ip int br" -p -o result.yaml
$ python task_4_3.py -y devices_task_4_3.yaml show "sh ip int br" -o result.txt""

"""
from concurrent.futures import ThreadPoolExecutor
import subprocess
from pprint import pprint
import yaml
from netmiko import ConnectHandler
from textfsm import clitable
import click


def ping_ip(ip):
    result = subprocess.run(["ping", "-c", "3", "-n", ip], stdout=subprocess.DEVNULL)
    ip_is_reachable = result.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, threads):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


def parse_command_dynamic(
    command_output, attributes_dict, index_file="index", templ_path="templates"
):

    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    return [dict(zip(cli_table.header, row)) for row in cli_table]


def send_cfg_commands(device, commands):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_config_set(commands)
    return result


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return result


def send_command_to_devices(devices, threads, show=None, config=None):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for device in devices:
            if show:
                futures.append(executor.submit(send_show_command, device, show))
            elif config:
                futures.append(executor.submit(send_cfg_commands, device, config))
        for device, future in zip(devices, futures):
            result_dict[device["host"]] = future.result()
    return result_dict


@click.group()
@click.option("--yaml-params", "-y", default="devices_task_4_3.yaml")
@click.option("--threads", "-t", default=5, type=click.IntRange(1, 10))
@click.pass_context
def manage_dev(context, yaml_params, threads):
    context.obj = {"yaml_params": yaml_params}
    context.obj.update({"threads": threads})


@manage_dev.command()
@click.argument("commands")
@click.pass_context
def config(context, commands):
    yaml_params = context.obj["yaml_params"]
    threads = context.obj["threads"]
    with open(yaml_params) as f:
        devices = yaml.safe_load(f)
    with open(commands) as f:
        config = f.readlines()
    pprint(send_command_to_devices(devices, threads, config=config))


@manage_dev.command()
@click.pass_context
def ping(context):
    yaml_params = context.obj["yaml_params"]
    with open(yaml_params) as f:
        devices = yaml.safe_load(f)
    threads = context.obj["threads"]
    ip_list = [device["host"] for device in devices]
    reach, unreach = ping_ip_addresses(ip_list, threads)
    print(
        f"""
Доступные адреса: {reach}
Недоступные адреса {unreach}"""
    )


@manage_dev.command()
@click.argument("show_command")
@click.option("--output-file", "-o")
@click.option("--parse", "-p", is_flag=True)
@click.pass_context
def show(context, show_command, output_file, parse):
    yaml_params = context.obj["yaml_params"]
    attributes_dict = {"Command": show_command, "Vendor": "cisco_ios"}
    with open(yaml_params) as f:
        devices = yaml.safe_load(f)
    ip_list = [device["host"] for device in devices]
    threads = context.obj["threads"]
    if output_file:
        with open(output_file, "w") as f:
            f.write(str(send_command_to_devices(devices, threads, show=show_command)))
    elif parse:
        output = send_command_to_devices(devices, threads, show=show_command)
        for ip in ip_list:
            pprint(parse_command_dynamic(output[ip], attributes_dict))
    elif output_file and parse:
        output = send_command_to_devices(devices, threads, show=show_command)
        parse_output = parse_command_dynamic(output, attributes_dict)
        with open(output_file, "w") as f:
            yaml.dump(parse_output, f)
    else:
        pprint(send_command_to_devices(devices, threads, show=show_command))


if __name__ == "__main__":
    manage_dev()
