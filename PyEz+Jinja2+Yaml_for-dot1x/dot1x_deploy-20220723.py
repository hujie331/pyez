from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml
# from jinja2 import Template
from pprint import pprint
import signal
import json
import sys
import time
import os
import keyboard
from getpass import getpass

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

def invalid_choice():
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print_one_by_one("      ~ Invalid Choice. Please try again. Thank you! ~\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    print()

def under_construction():
    print()
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print_one_by_one("~ This site is under construction. Please select another site, Thank you! ~\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    print()

def print_one_by_one(text):
    sys.stdout.write("\r " + " " * 60 + "\r")
    sys.stdout.flush()
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

def get_credentials():
    username = input('Username(Please input your AD credentials): ')
    password = getpass()
    return username, password

def set_cfg():
    dev = Device(host=host_ip, user=username, password=password, gather_facts=False).open()
    with Config(dev, mode='exclusive') as device_config:
        print('*' * 80)
        print_one_by_one(f'Loading configuration commands on {host_name} ({device_role}) located at {site_name}:\n')
        print_one_by_one('enable DHCP-security option to enable dhcp snooping. only for User/Dev wired networks for '
                         'now\nset interface range for dot1x ports\nset dot1x protocol. Server-reject-vlan to use '
                         'guest wired vlan\nconfigure radius server and profile\n')
        device_config.load(template_path=template_file, template_vars=vars, format='text')
        print('*' * 80)
        print_one_by_one(f'Comparing the candidate configuration to a previously committed configuration:\n')
        device_config.pdiff()
        print('*' * 80)
        pause = input("press 'Y' to commit the changes, or press 'N' to ignore the changes, or press 'Q' to exit: \n").lower()
        while True:
            if pause == 'y':
                print_one_by_one(f'you pressed Y, so committing {host_name} ({device_role}) located at {site_name}......\n')
                device_config.commit()
                print_one_by_one('commit succeeded')
                break

            elif pause == 'n':
                print("\nyou pressed N, so logging into next device...")
                break

            elif pause == 'q':
                print("\nyou pressed Q, so exit...")
                sys.exit(0)
            else:
                print('you input a wrong letter, skipping this device (no changes committed) and moving to the next one...')
                break
        print()
        print()
    dev.close()

os.system('clear')
username, password = get_credentials()

while True:
    site_choice = input("""\nPlease select teh site where you would like to deploy 802.1x: \n
       1:  SJCA_spare
       2:  Howard Hughes
       3:  San Francisco\n       
   Your choice: """)

    if site_choice == '1':
        inventory_file = "/home/jhu/PycharmProjects/pyez/set_ntp_name_syslog/inventory_sjca_spare.json"
        # vars_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_vars_hh.yml"
        # template_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_jinja2_template.j2"
        break
    elif site_choice == '2':
        inventory_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_inventory_hh.json"
        # vars_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_vars_hh.yml"
        # template_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_jinja2_template.j2"
        break
    elif site_choice == '3':
        under_construction()
    else:
        invalid_choice()

vars_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_vars_hh.yml"
template_file = "/home/jhu/PycharmProjects/pyez/PyEz+Jinja2+Yaml_for-dot1x/dot1x_jinja2_template.j2"
vars = yaml.load(open(vars_file), Loader=yaml.SafeLoader)

with open(inventory_file) as dev_file:
    devices = json.load(dev_file)  # convert json to dict

for device in devices:
    site_name = device["site name"]
    device_role = device["device role"]
    host_name = device["hostname"]
    host_ip = device["ip address"]


    dev = Device(host=host_ip, user=username, password=password, gather_facts=False).open()
    with Config(dev, mode='exclusive') as device_config:
        print('*' * 80)
        print_one_by_one(f'Loading configuration commands on {host_name} ({device_role}) located at {site_name}:\n')
        print_one_by_one('enable DHCP-security option to enable dhcp snooping. only for User/Dev wired networks for '
                         'now\nset interface range for dot1x ports\nset dot1x protocol. Server-reject-vlan to use '
                         'guest wired vlan\nconfigure radius server and profile\n')
        device_config.load(template_path=template_file, template_vars=vars, format='text')
        print('*' * 80)
        print_one_by_one(f'Comparing the candidate configuration to a previously committed configuration:\n')
        device_config.pdiff()
        print('*' * 80)
        
        pause = input(
            "press 'Y' to commit the changes, or press 'N' to ignore the changes, or press 'Q' to exit: \n").lower()
        while True:
            if pause == 'y':
                print_one_by_one(
                    f'you pressed Y, so committing {host_name} ({device_role}) located at {site_name}......\n')
                device_config.commit()
                print_one_by_one('commit succeeded')
                break

            elif pause == 'n':
                print("\nyou pressed N, so logging into next device...")
                break

            elif pause == 'q':
                print("\nyou pressed Q, so exit...")
                sys.exit(0)
            else:
                print(
                    'you input a wrong letter, skipping this device (no changes committed) and moving to the next one...')
                break
        print()
        print()
    dev.close()


print_one_by_one(f'The dot1x configurations for the devices located at {site_name} have been updated successfully!\n\n')