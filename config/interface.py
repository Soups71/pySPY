import os
from time import sleep
from datetime import datetime
from scapy import *
from scapy.all import *

class interface:
    def __init__(self, name):
        self.name = name
        self.channel = 1
        self.kill_changer = False
        self.file = ""
    def set_monitor_mode(self):
        os.system(f"ifconfig {self.name} down")
        os.system(f"iwconfig {self.name} mode monitor")
        os.system(f"ifconfig {self.name} up")
    def kill_changer(self):
        self.kill_changer = True
    def set_pcap(self):
        filename = datetime.now.strftime("%d_%m_%Y_%H_%M_%S_Channel_") + str(self.channel)+".pcap"
        self.file = PcapWriter(filename, append=True, sync=True)
    def sniffEAPOL(self, p):
        if(p.haslayer(EAPOL)):
            self.file.write(p)
            print("There's another packet")

    def sniffPackets(self):
        sniff(iface=self.name, prn=self.sniffEAPOL, count=0)

    def change_channel(self):
        while not self.kill_changer:
            os.system(f"iwconfig {self.name} channel {self.channel}")
            # switch channel from 1 to 14 each 0.5s
            print(f"Current channel: {self.channel}")
            self.channel = self.channel % 14 + 1
            sleep(0.5)