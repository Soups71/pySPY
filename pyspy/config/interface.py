import os
from time import sleep
from datetime import datetime
from scapy import *
from scapy.all import *
from termcolor import cprint

# Class for wifi card
class interface:
    def __init__(self, name):
        self.name = name
        self.channel = 1
        self.kill = False
        self.file = ""
        self.EAPOL_count = 0


    def set_monitor_mode(self):
        os.system(f"sudo ifconfig {self.name} down")
        os.system(f"sudo iwconfig {self.name} mode monitor")
        os.system(f"sudo ifconfig {self.name} up")

    def kill_changer(self):
        self.kill= True

    def set_pcap(self):
        filename = "pcaps/"+datetime.now().strftime("%d_%m_%Y_%H_%M_%S_Channel_") + str(self.channel)+".pcap"
        self.file = PcapWriter(filename, append=True, sync=True)

    def sniffEAPOL(self, p):
        if(p.haslayer(EAPOL)):
            self.file.write(p)
            self.EAPOL_count +=1
           
    def sniffPackets(self):
        while not self.kill:
            sniff(iface=self.name, prn=self.sniffEAPOL, count=200)
    
    def change_channel(self, ch):
            self.channel = ch
            os.system(f"sudo iwconfig {self.name} channel {self.channel}")
    
    def increment_channel(self):
        while not self.kill:
            self.channel = self.channel%14+1
            os.system(f"sudo iwconfig {self.name} channel {self.channel}")
            sleep(.2)
    def get_EAPOL_count(self):
        return self.EAPOL_count