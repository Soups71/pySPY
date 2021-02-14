from attacks import deauth
from config import interface, get_interfaces
from scapy import *
from scapy.all import *
from threading import Thread
important_channels = [1, 6, 11, 13]


if __name__ == "__main__":
    interfaces = []
    wireless_interfaces = get_interfaces()
    for each in wireless_interfaces:
        interfaces.append(interface(each))
    count = 0
    while(count < len(interfaces)):
        interfaces[count].channel = important_channels[count]
        count+=1
    for each in interfaces:
        each.set_pcap()
    processes = []
    current_process = 0
    for each in interfaces:
        processes.append(Thread(target=each.sniffPackets), current_process)
        processes[current_process].daemon = True
        processes[current_process].start()
        print(f"Capturing Packets with {each.name}")
    
    print("Capturing Packets!!!")
    while(True):
        shutdown = input("Would you like to stop capturing packets: ")
        if(shutdown.lower() == 'y'):
            for each in processes:
                each.join()
            break
    print("Goodbye")