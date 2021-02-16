from pyspy.callbacks.callback import getDF
from scapy.all import *
from threading import Thread
from pyspy.config import interface, get_interfaces
from pyspy.callbacks import get_hostnames, getDF
import time
import os


def print_all():
    while True:
        os.system("clear")
        print(getDF())
        time.sleep(0.5)

def main():
    # interface name, check using iwconfig
    interface_name = get_interfaces()[1]
    current_interface = interface(interface_name)
    current_interface.set_monitor_mode()
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start the channel changer
    channel_changer = Thread(target=current_interface.increment_channel)
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    sniff(prn=get_hostnames, iface=current_interface.name)


if __name__ == "__main__":
    main()