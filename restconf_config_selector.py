import logging
from typing import List

import requests
import yaml

import restconf_helpers

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('restconf.example')


def load_devices() -> List[dict]:
    with open('parameter_device.yaml', 'r') as host_file:
        hosts = yaml.load(host_file.read(), Loader=yaml.FullLoader)
        return hosts


def init_logger():
    _logger = logging.getLogger('restconf')
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)


def get_interfaces(host: dict) -> str:
    response = restconf_helpers.RestconfRequestHelper().get(
        url=f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/interface/',
        username=host['username'],
        password=host['password'])
    return response


def print_interfaces(host: dict) -> None:
    print(get_interfaces(host=host))


def get_bgpconfig(host: dict) -> str:
    response = restconf_helpers.RestconfRequestHelper().get(
        url=f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/router/bgp/',
        username=host['username'],
        password=host['password'])
    return response


def print_bpg(host: dict) -> None:
    print(get_bgpconfig(host=host))


def get_ospfconfig(host: dict) -> str:
    response = restconf_helpers.RestconfRequestHelper().get(
        url=f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/router/ospf/',
        username=host['username'],
        password=host['password'])
    return response


def print_ospf(host: dict) -> None:
    print(get_ospfconfig(host=host))


def main():
    devices = load_devices()

    logger.info(f'Getting information for device {devices}')
    print_interfaces(host=devices)
    print_bpg(host=devices)
    print_ospf(host=devices)


if __name__ == '__main__':
    init_logger()
    main()
