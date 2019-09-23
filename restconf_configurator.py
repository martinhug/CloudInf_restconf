import logging
from typing import List

import requests
import yaml

import restconf_helpers

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('restconf.example')

HEADERS = {
    'Content-Type': 'application/yang-data+xml',
    'Accept': 'application/yang-data+xml'
}


def load_devices() -> List[dict]:
    with open('device_infos.yaml', 'r') as host_file:
        hosts = yaml.load(host_file.read(), Loader=yaml.FullLoader)
        return hosts


def init_logger():
    _logger = logging.getLogger('restconf')
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)


def patch_interface_config(host, xml_payload):
    url = f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/interface/'

    response = requests.patch(url, auth=(host['username'], host['password']), data=xml_payload, headers=HEADERS,
                              verify=False)

    return response


def patch_ospf_config(host, xml_payload):
    url = f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/router/ospf/'

    response = requests.patch(url, auth=(host['username'], host['password']), data=xml_payload, headers=HEADERS,
                              verify=False)

    return response


def patch_bgp_config(host, xml_payload):
    url = f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/router/bgp/'

    response = requests.patch(url, auth=(host['username'], host['password']), data=xml_payload, headers=HEADERS,
                              verify=False)

    return response


def get_xml(filename):
    with open(filename) as xml_data:
        xml_payload = xml_data.read()

    return xml_payload


def main():
    devices = load_devices()
    for device in devices:
        logger.info(f'Configuring Interfaces for device {device["connection_address"]}')
        response_interface = patch_interface_config(device, get_xml("router_interface_config.xml"))
        print(response_interface)
        logger.info(f'Configuring OSPF for device {device["connection_address"]}')
        response_ospf = patch_ospf_config(device, get_xml("router_ospf_config.xml"))
        print(response_ospf)
        logger.info(f'Configuring BGP for device {device["connection_address"]}')
        response_bgp = patch_bgp_config(device, get_xml("router_bgp_config.xml"))
        print(response_bgp)


if __name__ == '__main__':
    init_logger()
    main()
