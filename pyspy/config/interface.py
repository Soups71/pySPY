import os
from time import sleep
from datetime import datetime
from scapy import *
from scapy.all import *

# Class for wifi card
class interface:
    # Initiate the object
    def __init__(self, name):
        self.name = name
        self.channel = 1
        self.kill = False
        self.file = ""
        self.packet_count = 0

    # Sets the interface into monitor mode
    def set_monitor_mode(self):
        os.system(f"sudo ifconfig {self.name} down")
        os.system(f"sudo iwconfig {self.name} mode monitor")
        os.system(f"sudo ifconfig {self.name} up")

    # Used to kill the multithreading 
    def kill_changer(self):
        self.kill= True

    # Sets the file name for the packet capture
    def set_pcap(self):
        filename = "pcaps/"+datetime.now().strftime("%d_%m_%Y_%H_%M_%S_Channel_") + str(self.channel)+".pcap"
        self.file = PcapWriter(filename, append=True, sync=True)

    # Used to save only the wifi handshakes
    def eapol_handler(self, p):
        if(p.haslayer(EAPOL)):
            self.file.write(p)
            self.packet_count +=1
    
    # Used to save all the packets
    def save_packet_handler(self, p):
        self.file.write(p)
        self.packet_count +=1

    # Used to sniff all the wifi handshakes
    def sniff_EAPOL_packets(self):
        while not self.kill:
            sniff(iface=self.name, prn=self.eapol_handler, count=200)

    # Used to sniff all the packets
    def sniff_all_packets(self):
        while not self.kill:
            sniff(iface=self.name, prn=self.save_packet_handler, count=200)

    # Used to change the channel
    def change_channel(self, ch):
            self.channel = ch
            os.system(f"sudo iwconfig {self.name} channel {self.channel}")
    
    # Used to update the channel
    def increment_channel(self):
        while not self.kill:
            self.channel = self.channel%14+1
            os.system(f"sudo iwconfig {self.name} channel {self.channel}")
            sleep(.2)