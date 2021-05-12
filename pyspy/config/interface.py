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
        self.channel_index = 0
        self.channels = []
        self.kill = False
        self.file = ""
        self.packet_count = 0
        self.eapol_packet_count = 0
        self.channel = 0

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
        try:
            # Gets current working directory
            path = os.getcwd()
            #Adds log path to log directory
            logging_path = os.path.join(path, "pcaps")
            # CHecks if the path exists; if not it makes it
            if(not os.path.isdir(logging_path)):
                os.mkdir(logging_path)
            # If error occurrs then we print to the console because its a bad thing
            # if this can't happen
        except OSError:
            print (f"Creation of the directory {path} failed")
            return -1
        filename = "pcaps/"+datetime.now().strftime("%d_%m_%Y_%H_%M_%S_Channel_") + str(self.channel)+".pcap"
        self.file = PcapWriter(filename, append=True, sync=True)

    # Used to save only the wifi handshakes
    def eapol_handler(self, p):
        if(p.haslayer(EAPOL)):
            self.file.write(p)
            self.eapol_packet_count +=1
            self.packet_count += 1
    
    # Used to save all the packets
    def save_packet_handler(self, p):
        self.file.write(p)
        if(p.haslayer(EAPOL)):
            self.eapol_packet_count +=1
        self.packet_count +=1

    # Used to sniff all the wifi handshakes
    def sniff_EAPOL_packets(self):
        while not self.kill:
            sniff(iface=self.name, prn=self.eapol_handler, count=200)

    # Used to sniff all the packets
    def sniff_all_packets(self):
        while not self.kill:
            sniff(iface=self.name, prn=self.save_packet_handler, count=200)

    # Set channel range
    def set_channel_range(self, range):
        # Range is an array of integer values
        self.channels = range

    # Used to change the channel
    def change_channel(self, ch):
            self.channel = ch
            os.system(f"sudo iwconfig {self.name} channel {self.channel}")
    
    # Used to update the channel
    def increment_channel_auto(self):
        while not self.kill:
            self.change_channel(self.channels[self.channel_index])
            self.channel_index += 1
            if self.channel_index >= len(self.channels):
                self.channel_index = 0
            sleep(.2)
    # Used to update the channel
    def increment_channel_manually(self):
        self.change_channel(self.channels[self.channel_index])
        self.channel_index += 1
        if self.channel_index >= len(self.channels):
            self.channel_index = 0