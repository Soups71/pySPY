from pyspy.config.config import print_good
from scapy.all import *
from threading import Thread
from pyspy.config import interface, get_interfaces, banner, print_update, print_warning, get_AP_scanner_args
from pyspy.callbacks import get_hostnames, getDF, save_results
import os
keep_going = True

def print_all():
    global keep_going
    while keep_going:
        os.system("clear")
        print(getDF())
        print_good("[+] Exit by typing y and hitting enter")
        time.sleep(0.5)

def get_input():
    global keep_going
    while keep_going:
        print_update("[+] Do you want to stop (y/N): ", False)
        stop = input()
        if stop.lower() =='y':
            print_warning("[+] Stopping soon")
            keep_going = False

def main(arguments):
    global keep_going
    # interface name, check using iwconfig
    if arguments.interface != None:
        interface_name = arguments.interface
    else:
        interface_name = get_interfaces()[1]

    current_interface = interface(interface_name)
    if not arguments.quiet:
        print_update("[+] Putting the interface into monitor mode")
    current_interface.set_monitor_mode()
    print_good("[+] Begining AP Scan")
    if not arguments.write:
        # start the thread that prints all the networks
        printer = Thread(target=print_all)
        printer.daemon = True
        printer.start()
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
    current_interface.kill_changer()
    if arguments.write:
        save_results(arguments.write)
    if not arguments.write:
        printer.join()
    user_input.join()
    channel_changer.join()
if __name__ == "__main__":
    cli_arguments = get_AP_scanner_args()
    if  not cli_arguments.quiet:
        banner()
    main(cli_arguments)