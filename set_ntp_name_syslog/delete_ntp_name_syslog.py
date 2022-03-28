import json
import sys
import time
import os
from getpass import getpass

from jnpr.junos import Device
from jnpr.junos.utils.config import Config


def print_one_by_one(text):
    sys.stdout.write("\r " + " " * 60 + "\r")
    sys.stdout.flush()
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

def delete_cfg():
    with Config(device_connection, mode='exclusive') as device_config:
        print('*' * 80)
        print_one_by_one(f'Loading configuration commands on {host_name} ({device_role}) located at {site_name}:\n')
        print_one_by_one('delete system ntp server 172.31.24.57\ndelete system name-server 172.31.24.53\ndelete '
                         'system syslog host 10.126.63.40 any any\n')
        device_config.load('delete system ntp server 172.31.24.57', format='set')
        device_config.load('delete system name-server 172.31.24.53', format='set')
        device_config.load('delete system syslog host 10.126.63.40 any any', format='set')
        print('*' * 80)
        print_one_by_one(f'Comparing the candidate configuration to a previously committed configuration:\n')
        device_config.pdiff()
        print('*' * 80)
        print_one_by_one(f'committing......\n')
        device_config.commit()
        print_one_by_one('commit succeeded')
        print()
        print()
    device_connection.close()

def get_credentials():
    username = input('Username(Please input your AD credentials): ')
    password = getpass()
    return username, password

os.system('clear')
username, password = get_credentials()

#devices = ['172.19.195.47', '172.19.195.37', '172.19.195.38', '172.19.195.39']
inventory_file = "/home/jhu/PycharmProjects/pyez/set_ntp_name_syslog/inventory_sjca_spare.json"

with open(inventory_file) as dev_file:
    devices = json.load(dev_file)  # convert json to dict

for device in devices:
    site_name = device["site name"]
    device_role = device["device role"]
    host_name = device["hostname"]
    host_ip = device["ip address"]
    device_connection = Device(host=host_ip, user=username, password=password).open()
    delete_cfg()

print_one_by_one(f'The configurations for the devices located at {site_name} have been updated successfully!\n\n')