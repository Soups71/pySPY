#!/usr/bin/python3
# Imports
from pyspy.config import interface, get_interfaces, get_handshake_args, banner, get_2ghz_channels, get_5ghz_channels, get_channels
from pyspy.config import print_warning, print_update, print_good
from scapy import *
from scapy.all import *
from threading import Thread


def handshake(arguments):
    important_channels = []
    # Most common wifi channels
    if arguments.frequency == 2:
        important_channels = get_2ghz_channels()
    elif arguments.frequency == 5:
        important_channels = get_5ghz_channels()
    else:
        important_channels = get_channels()

    # Update important channels if other channels were passed
    if(len(arguments.channel)>=1):
        important_channels = arguments.channel

    # List to hold the interface objects
    interfaces = []

    # Update important channels if other channels were passed
    if(len(arguments.channel)>=1):
        important_channels = arguments.channel
        
    # Get every wifi interface other than the built in wifi card
    wireless_interfaces = get_interfaces()[1:]
    if wireless_interfaces == []:
        print_warning("[+] Could not find any wireless cards")
        return -1
    # Create an interface object for each interface card
    for each in wireless_interfaces:
        interfaces.append(interface(each))
    
    # Checks for indifference int he list lengths
    if(len(interfaces)>len(important_channels)):
        print_warning("[+] Not every interface will be used")
    elif(len(interfaces)<len(important_channels)):
        print_warning("[+] Not every channel will be used for capture. EAPOL packets will be missed")
    
    # This loop just allows for us to put each interface on a different channel
    count = 0
    while(count < len(interfaces)):
        interfaces[count].set_monitor_mode()
        interfaces[count].change_channel(important_channels[count])
        count+=1

    # Sets the file to save the EAPOL packets to
    for each in interfaces:
        each.set_pcap()

    # Multi threading the capture process for each antenna
    processes = []
    current_process = 0
    for each in interfaces:
        if arguments.eapol:
            processes.append(Thread(target=each.sniff_EAPOL_packets))
        else:
            processes.append(Thread(target=each.sniff_all_packets))
        processes[current_process].daemon = True
        processes[current_process].start()
        if(not arguments.quiet):
            print_update(f"[+] Capturing Packets with {each.name} on channel {each.channel}")
        current_process +=1

    # This doesn't work to stop it but it trys it's best
    while(True):
        print_good("[+] Get update? (Y/n/exit): ", False)
        user_input = input()
        if user_input.lower() == 'y' or user_input.lower() == '':
            for each in interfaces:
                print_good(f"[+] {each.packet_count}  packets captured on channel {each.channel}")
        elif(user_input.lower() == 'exit'):
            print_update("[+] Starting exit protocol. Just sit back and relax.")
            for each in interfaces:
                # Allows for it to close cleanly
                each.kill_changer()
            break
    # Cleans up the threads
    for each in processes:
                each.join()

    if(not arguments.quiet):
            print_good("[+] Goodbye. Thanks for using this program")


# Start of main program
if __name__ == "__main__":
    cli_arguments = get_handshake_args()
    if not cli_arguments.quiet:
        banner()
        print_good("[+] Begining initialization sequence to collect handshakes")
    if os.geteuid() == 0:
        handshake(cli_arguments)
    else:
        print_warning("[+] This program must be ran as root!!!")