import pandas
from scapy import *
from scapy.all import *


networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)
pandas.set_option("display.max_rows", None)
# Function to save the data frame
def save_results(filename):
    networks.to_csv(filename)

# Gets the data out of the packets
def get_hostnames(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        crypto = str(crypto).strip("{'").strip("'}")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)

# Function to send dataframe back to the main program
def getDF():
    sorted_network = networks.sort_values("dBm_Signal", ascending=False)
    return sorted_network