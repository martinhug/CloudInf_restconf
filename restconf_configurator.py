import logging
from typing import List

import requests
import yaml

from jinja2 import Environment, FileSystemLoader

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('restconf.configurator')


def init_logger():
    _logger = logging.getLogger('restconf')
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)


HEADERS = {
    'Content-Type': 'application/yang-data+xml',
    'Accept': 'application/yang-data+xml'
}


def load_yaml(filename) -> List[dict]:
    with open(filename, 'r') as host_file:
        hosts = yaml.load(host_file.read(), Loader=yaml.FullLoader)
        return hosts


def load_template(xml_template):
    env = Environment(loader=FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(xml_template)
    return template


def patch_config(host, xml_payload, url):
    response = requests.patch(url.format(device=host["connection_address"]), auth=(host['username'], host['password']),
                              data=xml_payload, headers=HEADERS,
                              verify=False)

    return response


def main():
    devices = load_yaml('parameter_device.yaml')
    urls = load_yaml('parameter_restconf_URLs.yaml')

    logger.info(f'Start to Configure device:  {devices["connection_address"]}')

    logger.info(f'Configuring Loopbacks...')
    loopback = load_yaml('parameter_loopback.yaml')
    for loop in loopback:
        template = load_template('jinja_template_interfaces.xml')
        response_interface = patch_config(devices, template.render(loop), urls['interface'])
        logger.info('Loopbacks finished Result: ' + response_interface.__str__())

    logger.info('Configuring OSPF... ')
    ospf = load_yaml('parameter_ospf.yaml')
    for network in ospf:
        template = load_template('jinja_template_ospf.xml')
        response_ospf = patch_config(devices, template.render(network), urls['ospf'])
        logger.info('OSPF finished Result: ' + response_ospf.__str__())

    logger.info('Configuring BGP... ')
    bgp_config = load_yaml('parameter_bgp.yaml')
    for neighbor in bgp_config:
        template = load_template('jinja_template_bgp.xml')
        response_bgp = patch_config(devices, template.render(neighbor), urls['bgp'])
        logger.info('BGP finished Result: ' + response_bgp.__str__())

    logger.info('Configuration completed')


if __name__ == '__main__':
    init_logger()
    main()
