import pytest
import yaml
from task_1_2 import Network

# Parametrizing fixtures example
# ip_list = ["10.10.10.0/24", "40.40.40.0/30"]
#
#
# @pytest.fixture(params=ip_list)
# def new_net(request):
#    net = Network(request.param)
#    return net

with open("devices.yaml") as f:
    devices = yaml.safe_load(f)

secret_params_list = [
    {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    },
    {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "ciscoi",
    },
    {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
    },
]


@pytest.fixture()
def new_net():
    net = Network("10.10.10.0/29")
    return net


@pytest.fixture()
def all_addresses():
    addresses = (
        "10.10.10.1",
        "10.10.10.2",
        "10.10.10.3",
        "10.10.10.4",
        "10.10.10.5",
        "10.10.10.6",
    )
    return addresses


@pytest.fixture()
def first_dev_params():
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    return devices[0]


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


@pytest.fixture(params=secret_params_list)
def secret_params(request):
    return request.param


@pytest.fixture()
def correct_params():
    r1_params = {
        "host": "192.168.122.101",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    return r1_params
