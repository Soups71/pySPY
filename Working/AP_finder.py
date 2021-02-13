from scapy.all import *
from threading import Thread
import pandas
import time
import os
import psutil

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

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


def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)


def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(0.5)

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


if __name__ == "__main__":
    # interface name, check using iwconfig
    interface = get_interfaces()[1]
    print(interface)
    change_mode(interface)
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)