import os
import psutil
from termcolor import cprint

def print_warning(output):
    cprint(output, 'red')
def print_good(output):
    cprint(output, 'green')
def print_update(output):
    cprint(output, 'yellow')

def get_interfaces():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    wireless_interfaces = []
    for intface, addr_list in addresses.items():
        if  intface[:2] == "wl":
            wireless_interfaces.append(intface)
    return wireless_interfaces