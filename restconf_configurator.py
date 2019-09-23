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

def patch_new_interface_to_host(host, xml_payload):
    url = f'https://{host["connection_address"]}/restconf/data/Cisco-IOS-XE-native:native/interface/'

    response = requests.patch(url, auth=(host['username'], host['password']), data=xml_payload, headers=HEADERS, verify=False)

    return response

def get_xml(filename):
    with open(filename) as xml_data:
        xml_payload = xml_data.read()

    return xml_payload

def main():
    devices = load_devices()
    for device in devices:
        logger.info(f'Configuring Interfaces for device {device}')
        router_config_payload = get_xml("router_interfaces_config.xml")
        response_interface = patch_new_interface_to_host(device, router_config_payload)
        print(response_interface)

if __name__ == '__main__':
    init_logger()
    main()
