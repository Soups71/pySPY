# Imports
from pyspy.config import interface, get_interfaces, get_handshake_args, banner
from pyspy.config import print_warning, print_update, print_good
from scapy import *
from scapy.all import *
from threading import Thread


def main(arguments):
    # Most common wifi channels
    important_channels = [1, 6, 11, 12, 13]
    # Update important channels if other channels were passed
    if(len(arguments.channel)>=1):
        important_channels = arguments.channel
    interfaces = []
    # Get every wifi interface other than the built in wifi card
    wireless_interfaces = get_interfaces()[1:]
    # Create an interface object for each interface card
    for each in wireless_interfaces:
        interfaces.append(interface(each))
    # This loop just allows for us to put each interface on a different channel
    count = 0
    if(len(interfaces)>len(important_channels)):
        print_warning("[+] Not every interface will be used")
    elif(len(interfaces)<len(important_channels)):
        print_warning("[+] Not every channel will be used for capture. EAPOL packets will be missed")
    while(count < len(interfaces)):
        interfaces[count].set_monitor_mode()
        interfaces[count].change_channel(important_channels[count])
        count+=1
    # Sets the file to save the EAPOL packets to
    for each in interfaces:
        each.set_pcap()
    # Multi threading tyhe capture process for each antenna
    processes = []
    current_process = 0
    for each in interfaces:
        processes.append(Thread(target=each.sniffPackets))
        processes[current_process].daemon = True
        processes[current_process].start()
        if(not arguments.quiet):
            print_update(f"[+] Capturing Packets with {each.name} on channel {each.channel}")
        current_process +=1
    # This doesn't work to stop it but it trys it's best
    while(True):
        print_good("[+] Would you like to stop capturing packets (y/N): ", False)
        shutdown = input()
        if(shutdown.lower() == 'y'):
            for each in interfaces:
                each.kill_changer()
            break
    for each in processes:
                each.join()
    if(not arguments.quiet):
            print_good("Goodbye")


# Start of main program
if __name__ == "__main__":
    cli_arguments = get_handshake_args()
    if not cli_arguments.quiet:
        banner()
        print_good("[+] Begining initialization sequence to collect handshakes")
    main(cli_arguments)