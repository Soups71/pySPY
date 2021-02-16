import os
from time import sleep
from datetime import datetime
from scapy import *
from scapy.all import *
from termcolor import cprint

class interface:
    def __init__(self, name):
        self.name = name
        self.channel = 1
        self.kill_changer = False
        self.file = ""
    def set_monitor_mode(self):
        os.system(f"sudo ifconfig {self.name} down")
        os.system(f"sudo iwconfig {self.name} mode monitor")
        os.system(f"sudo ifconfig {self.name} up")
    def kill_changer(self):
        self.kill_changer = True
    def set_pcap(self):
        filename = "pcaps/"+datetime.now().strftime("%d_%m_%Y_%H_%M_%S_Channel_") + str(self.channel)+".pcap"
        self.file = PcapWriter(filename, append=True, sync=True)
    def sniffEAPOL(self, p):
        if(p.haslayer(EAPOL)):
            self.file.write(p)
            cprint(f"[+] EAPOL packet captured on channel {self.channel}", "green")

    def sniffPackets(self):
        sniff(iface=self.name, prn=self.sniffEAPOL, count=0)

    def change_channel(self, ch):
            self.channel = ch
            os.system(f"sudo iwconfig {self.name} channel {self.channel}")