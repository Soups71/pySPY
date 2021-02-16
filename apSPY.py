from scapy.all import *
from threading import Thread
from pyspy.config import interface, get_interfaces, banner, print_update, print_warning, get_AP_scanner_args
from pyspy.callbacks import get_hostnames, getDF, save_results
import os

keep_going = True

def print_all():
    while True:
        os.system("clear")
        print(getDF())
        time.sleep(0.5)

def get_input():
    while not keep_going:
        print_update("Do you want to stop(N/y): ")
        stop = input()
        if stop.lower() =='y':
            print_warning("[+] Stopping soon")
            keep_going = False

def main(arguments):
    # interface name, check using iwconfig
    if arguments.interface != None:
        interface_name = arguments.interface
    else:
        interface_name = get_interfaces()[1]

    current_interface = interface(interface_name)
    if not arguments.quiet:
        print_update("Putting the interface into monitor mode")
    current_interface.set_monitor_mode()
    if arguments.write == None:
        # start the thread that prints all the networks
        printer = Thread(target=print_all)
        printer.daemon = True
        printer.start()
    else:
        user_input = Thread(target=get_input)
        user_input.daemon = True
        user_input.start()
    # start the channel changer
    channel_changer = Thread(target=current_interface.increment_channel)
    channel_changer.daemon = True
    channel_changer.start()
    while keep_going:
        # start sniffing
        sniff(prn=get_hostnames, iface=current_interface.name, count = 100)
    if arguments.write != None:
        save_results(arguments.write)
    print_update("[+] Please hit ctrl-C inorder to stop the program")
if __name__ == "__main__":
    cli_arguments = get_AP_scanner_args()
    if  not cli_arguments.quiet:
        banner()
    main(cli_arguments)