# -*- coding: utf-8 -*-
"""
Задание 1.1

Написать тест или тесты для функции get_int_vlan_map. Тест должен проверять:

* тип возвращаемых данных
* что словари, которые возвращает функция, содержат правильные данные

Проверить работу функции с разными входящими данными и убедиться, что словари
генерируются правильно для этих данных.
Пример вызова функции показан в файле заданий.

Тест(ы) написать в файле заданий.

Ограничение: функцию менять нельзя.
Для заданий этого раздела нет тестов для проверки тестов :)
"""
from pprint import pprint
import pytest

access_dict1 = {
    "FastEthernet0/0": 10,
    "FastEthernet0/2": 20,
    "FastEthernet1/0": 20,
    "FastEthernet1/1": 30,
    "FastEthernet1/3": 1,
}

trunk_dict1 = {
    "FastEthernet0/1": [100, 200],
    "FastEthernet0/3": [100, 300, 400, 500, 600],
    "FastEthernet1/2": [400, 500, 600],
}

access_dict2 = {
    "FastEthernet0/0": 10,
    "FastEthernet0/2": 20,
    "FastEthernet1/0": 20,
    "FastEthernet1/1": 30,
    "FastEthernet1/3": 1,
    "FastEthernet2/0": 1,
    "FastEthernet2/1": 1,
}

trunk_dict2 = {
    "FastEthernet0/1": [100, 200],
    "FastEthernet0/3": [100, 300, 400, 500, 600],
    "FastEthernet1/2": [400, 500, 600],
}


@pytest.mark.parametrize("file_name", ["config_sw1.txt", "config_sw1.txt"])
def test_return_type(file_name):
    with open(file_name) as f:
        output = f.read()
    access, trunk = get_int_vlan_map(output)
    assert type(access) == dict and type(trunk) == dict


@pytest.mark.parametrize(
   ("file_name", "access_dict", "trunk_dict"),
   [
       ("config_sw1.txt", access_dict1, trunk_dict1),
       ("config_sw2.txt", access_dict2, trunk_dict2),
   ],
)
def test_dicts(file_name, access_dict, trunk_dict):
    with open(file_name) as f:
        output = f.read()
    access_dict_out, trunk_dict_out = get_int_vlan_map(output)
    assert access_dict_out == access_dict and trunk_dict_out ==trunk_dict


def get_int_vlan_map(config_as_str):
    access_port_dict = {}
    trunk_port_dict = {}
    for line in config_as_str.splitlines():
        if line.startswith("interface") and "Ethernet" in line:
            current_interface = line.split()[-1]
            access_port_dict[current_interface] = 1
        elif "switchport access vlan" in line:
            access_port_dict[current_interface] = int(line.split()[-1])
        elif "switchport trunk allowed vlan" in line:
            vlans = [int(i) for i in line.split()[-1].split(",")]
            trunk_port_dict[current_interface] = vlans
            del access_port_dict[current_interface]
    return access_port_dict, trunk_port_dict


if __name__ == "__main__":
    with open("config_sw2.txt") as f:
        pprint(get_int_vlan_map(f.read()))
#    with open("config_sw2.txt") as f:
#        pprint(get_int_vlan_map(f.read()))
