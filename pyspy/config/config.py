import psutil
from termcolor import cprint

def print_warning(output, newline=True):
    if newline:
        cprint(output, 'red')
    else:
        cprint(output, 'red', end='')
def print_good(output, newline=True):
    if newline:
        cprint(output, 'green')
    else:
        cprint(output, 'green', end='')
def print_update(output, newline=True):
    if newline:
        cprint(output, 'yellow')
    else:
        cprint(output, 'yellow', end='')

def get_interfaces():
    addresses = psutil.net_if_addrs()
    wireless_interfaces = []
    for intface, addr_list in addresses.items():
        if  intface[:2] == "wl":
            wireless_interfaces.append(intface)
    return wireless_interfaces