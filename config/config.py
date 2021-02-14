import os
import psutil


def get_interfaces():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    wireless_interfaces = []
    for intface, addr_list in addresses.items():
        if  intface[:2] == "wl":
            wireless_interfaces.append(intface)
    return wireless_interfaces