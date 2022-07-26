# -*- coding: utf-8 -*-
"""
Задание 1.2

Написать тесты для класса Network. Тесты должны проверять:

* переменные экземпляров network и addresses:
  * наличие переменной экземпляра
  * правильное значение

* метод __iter__:
  * метод есть
  * возвращает итератор
  * при итерации возвращаются IP-адреса и правильные IP-адреса (достаточно проверить 2 адреса)

* метод __len__:
  * проверка количества IP-адресов

* метод __getitem__:
  * проверить обращение по положительному, отрицательному индексу
  * проверить, что при обращении к не существующему индексу, генерируется исключение IndexError


Тесты написать в файле заданий. Разделить на тесты по своему усмотрению.

Ограничение: класс менять нельзя.
Для заданий этого раздела нет тестов для проверки тестов :)
"""
import ipaddress
import pytest
from collections.abc import Iterable, Iterator


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


def test_variables(new_net):
    assert getattr(new_net, "network", None) != None, "Attribute doesn't exist"
    assert getattr(new_net, "addresses", None) != None, "Attribute doesn't exist"

def test_values(new_net, all_addresses):
    assert new_net.network == "10.10.10.0/29", "Network attribute is wrong"
    assert new_net.addresses == all_addresses, "Address attribute is wrong"

def test_iter(new_net):
    iter_net = new_net.__iter__()
    assert getattr(new_net, "__iter__", None) != None, "Attribute doesn't exist"
    assert isinstance(new_net.__iter__(), Iterator) == True, "__iter__ doesn't return Iterator"
    assert next(iter_net) == "10.10.10.1" and next(iter_net) == "10.10.10.2", "Iter returns wrong address"

def test_len(new_net):
    assert new_net.__len__() == 6, "__len__ returns wrong value"


def test_getitem(new_net):
    assert new_net[1] == "10.10.10.2"
    assert new_net[-1] == "10.10.10.6"


class Network:
    def __init__(self, network):
        self.network = network
        subnet = ipaddress.ip_network(self.network)
        self.addresses = tuple([str(ip) for ip in subnet.hosts()])

    def __iter__(self):
        return iter(self.addresses)

    def __len__(self):
        return len(self.addresses)

    def __getitem__(self, index):
        return self.addresses[index]


if __name__ == "__main__":
    # пример создания экземпляра
    net1 = Network("10.1.1.192/30")
