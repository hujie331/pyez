import json
import sys
import time
import os
import keyboard
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

def set_cfg():
    with Config(device_connection, mode='exclusive') as device_config:
        print('*' * 80)
        print_one_by_one(f'Loading configuration commands on {host_name} ({device_role}) located at {site_name}:\n')
        print_one_by_one('enable DHCP-security option to enable dhcp snooping. only for User/Dev wired networks for '
                         'now\nset interface range for dot1x ports\nset dot1x protocol. Server-reject-vlan to use '
                         'guest wired vlan\nconfigure radius server and profile\n')
        device_config.load(f'set vlans {user_vlan_name} vlan-id {user_vlan_id} forwarding-options dhcp-security', format='set')
        device_config.load(f'set vlans {dev_vlan_name} vlan-id {dev_vlan_id} forwarding-options dhcp-security', format='set')
        device_config.load(f'set interfaces interface-range dot1x-range member {dot1x_range_member}', format='set')
        device_config.load('set protocols dot1x authenticator authentication-profile-name nac-clients', format='set')
        device_config.load('set protocols dot1x authenticator interface dot1x-range supplicant multiple', format='set')
        device_config.load('set protocols dot1x authenticator interface dot1x-range transmit-period 3', format='set')
        device_config.load('set protocols dot1x authenticator interface dot1x-range mac-radius', format='set')
        device_config.load('set protocols dot1x authenticator interface dot1x-range reauthentication 3600', format='set')
        device_config.load(f'set protocols dot1x authenticator interface dot1x-range server-reject-vlan {guest_wired_vlan}', format='set')
        device_config.load('set protocols dot1x authenticator interface dot1x-range server-fail permit', format='set')
        device_config.load(f'set access radius-server {local_pps_vip} accounting-port 1813', format='set')
        device_config.load(f'set access radius-server {local_pps_vip}  secret {radius_secret}', format='set')
        device_config.load(f'set access radius-server {local_pps_vip}  timeout 5', format='set')
        device_config.load(f'set access radius-server {local_pps_vip}  retry 2', format='set')
        device_config.load('set access radius-server 10.50.81.24 accounting-port 1813', format='set')
        device_config.load(f'set access radius-server 10.50.81.24 secret {radius_secret}', format='set')
        device_config.load('set access radius-server 10.50.81.24 timeout 5', format='set')
        device_config.load('set access radius-server 10.50.81.24 retry 2', format='set')
        device_config.load('set access profile nac-clients authentication-order radius', format='set')
        device_config.load('set access profile nac-clients radius authentication-server 7.7.7.7', format='set')
        device_config.load('set access profile nac-clients radius authentication-server 10.50.81.24', format='set')
        device_config.load('set access profile nac-clients radius accounting-server 7.7.7.7', format='set')
        device_config.load('set access profile nac-clients radius accounting-server 10.50.81.24', format='set')
        device_config.load('set access profile nac-clients accounting order radius', format='set')
        device_config.load('set access profile nac-clients accounting coa-immediate-update', format='set')
        device_config.load('set access profile nac-clients accounting address-change-immediate-update', format='set')
        print('*' * 80)
        print_one_by_one(f'Comparing the candidate configuration to a previously committed configuration:\n')
        device_config.pdiff()
        print('*' * 80)
        pause = input("press 'Y' to commit the changes, or press 'N' to ignore the changes, or press 'Q' to exit: \n").lower()
        while True:
            if pause == 'y':
                print_one_by_one(f'committing {host_name} ({device_role}) located at {site_name}......\n')
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
                print('you input a wrong letter, skipping this device (no changes committed) and moving to the next one')
                break
        print()
        print()
    device_connection.close()


def get_credentials():
    username = input('Username(Please input your AD credentials): ')
    password = getpass()
    return username, password

os.system('clear')
sitename = input('which site you want to apply the changes to? \n')
print()
uservlanname = input('what is the user vlan name? \n')
print()
usrvlanid = input('what is the user vlan id? \n')
print()
devvlanname = input('what is the dev vlan name? \n')
print()
devvlanid = input('what is the dev vlan id? \n')
print()
dot1xrangemember = input('please input the dot1x range member: \n')
print()
localppsvip = input('please input the local pps vip: \n')
print()
radiussecret = input('please copy radius secret from 1pass and paste here: \n')

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
    user_vlan_name = "USER-VLAN"
    user_vlan_id = "777"
    dev_vlan_name = "DEV-VLAN"
    dev_vlan_id = "666"
    guest_wired_vlan = "USER-VLAN"
    dot1x_range_member = "ge-0/0/40"
    local_pps_vip = "7.7.7.7"
    radius_secret = "802.1x-juniper-radius-secret"
    device_connection = Device(host=host_ip, user=username, password=password).open()
    set_cfg()


print_one_by_one(f'The dot1x configurations for the devices located at {site_name} have been updated successfully!\n\n')