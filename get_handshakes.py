# Imports
from pyspy.config import interface, get_interfaces
from scapy import *
from scapy.all import *
from threading import Thread
# Most common wifi channels
important_channels = [1, 6, 11, 13]

# Start of main program
if __name__ == "__main__":
    interfaces = []
    # Get every wifi interface other than the built in wifi card
    wireless_interfaces = get_interfaces()[1:]
    # Create an interface object for each interface card
    for each in wireless_interfaces:
        interfaces.append(interface(each))
    # This loop just allows for us to put each interface on a different channel
    count = 0
    while(count < len(interfaces)):
        interfaces[count].channel = important_channels[count]
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
        print(f"Capturing Packets with {each.name}")
        current_process +=1
    print("Capturing Packets!!!")
    # This doesn't work to stop it but it trys it's best
    while(True):
        shutdown = input("Would you like to stop capturing packets: ")
        if(shutdown.lower() == 'y'):
            for each in processes:
                each.join()
            break
    print("Goodbye")