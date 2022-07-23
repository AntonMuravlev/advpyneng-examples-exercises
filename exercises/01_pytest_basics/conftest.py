import pytest
from task_1_2 import Network

# Parametrizing fixtures example
# ip_list = ["10.10.10.0/24", "40.40.40.0/30"]
#
#
# @pytest.fixture(params=ip_list)
# def new_net(request):
#    net = Network(request.param)
#    return net


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
