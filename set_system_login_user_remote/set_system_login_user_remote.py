import json
import sys
import time
import os
from getpass import getpass
from pprint import pprint

from jnpr.junos import Device
from jnpr.junos.utils.config import Config


def print_one_by_one(text):
    sys.stdout.write("\r " + " " * 60 + "\r")
    sys.stdout.flush()
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)


def set_cfg():
    with Config(dev, mode='exclusive') as device_config:
        print('*' * 80)

        print_one_by_one(f'Entering configuration exclusive mode and loading configuration commands on {host_name} ({device_role}) located at {site_name}:\n')
        # device_config.lock()
        print_one_by_one('set system login user remote class operator\n')
        device_config.load('set system login user remote class operator', format='set')
        print('*' * 80)
        print_one_by_one('Comparing the candidate configuration to a previously committed configuration:\n')
        device_config.pdiff()
        print('*' * 80)
        print_one_by_one('Committing......\n')
        device_config.commit()
        print_one_by_one('Commit succeeded and logging out of the device')
        print()
        print()



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
    dev = Device(host=host_ip, user=username, password=password).open()
    device_cfg = dev.rpc.get_config(options={'format': 'json'})
    user_list = device_cfg['configuration']['system']['login']['user']
    # pprint(user_list)
    user_name_list = []
    for user in user_list:
        user_name_list.append(user['name'])

    if 'remote' not in user_name_list:
        set_cfg()
    else:
        print()
        print(f'{host_name} is already configured the user "remote"')
    print()
    print('*' * 80)
    print()
    dev.close()



print_one_by_one(f'The configurations for the devices located at {site_name} have been updated successfully!\n\n')