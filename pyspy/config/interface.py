import os
from time import sleep
from datetime import datetime
from scapy import *
from scapy.all import *
from pylibpcap.base import Sniff

# Class for wifi card
class interface:
    # Initiate the object
    def __init__(self, name):
        self.name = name
        self.channel_index = 0
        self.channels = []
        self.kill = False
        self.file = ""
        self.file_name = ""
        self.packet_count = 0
        self.eapol_packet_count = 0
        self.channel = 0
        self.packet_buf = []

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
        self.file_name = "pcaps/"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S_Channel_") + str(self.channel)+".pcap"
        self.file = PcapWriter(self.file_name, append=True, sync=True)

    # Used to save only the wifi handshakes
    def eapol_handler(self, p):
        if(p.haslayer(EAPOL)):
            self.packet_buf.append(p)
            self.eapol_packet_count +=1
            self.packet_count += 1
            if len(self.packet_buf) == 1000:
                self.save_to_file()
    
    # Used to save all the packets
    def save_packet_handler(self, p):
        self.packet_buf.append(p)
        if(p.haslayer(EAPOL)):
            self.eapol_packet_count +=1
        self.packet_count +=1
        if len(self.packet_buf) == 1000:
            self.save_to_file()

    def save_to_file(self):
        for each in self.packet_buf:
            self.file.write(each)
        self.packet_buf = []

    # Used to sniff all the wifi handshakes
    def sniff_EAPOL_packets(self):
        check = 0
        sniffobj = Sniff(self.name, count=100, promisc=1, out_file=self.file_name)
        while not self.kill:
            for plen, t, buf in sniffobj.capture():
                self.packet_count+=1
                if check == 100:
                    check = 0
                    break
                else:
                    check+=1
            # sniff(iface=self.name, prn=self.eapol_handler, count=200)
        sniffobj.close()
            

    # Used to sniff all the packets
    def sniff_all_packets(self):
        check = 0
        sniffobj = Sniff(self.name, count=-1, promisc=1, out_file=self.file_name)
        while not self.kill:
            for plen, t, buf in sniffobj.capture():
                self.packet_count+=1
                if check == 100:
                    check = 0
                    break
                else:
                    check+=1
            # sniff(iface=self.name, prn=self.save_packet_handler, count=200)
        sniffobj.close()

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