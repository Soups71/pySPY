import argparse
from termcolor import cprint
from pyspy.config import get_interfaces
import re

def valid_filename(prospective_filename):
    return bool(re.match("^[A-Za-z0-9_]*$", prospective_filename))

def valid_interface(prospective_interface):
    possible_interfaces = get_interfaces()
    return(prospective_interface in possible_interfaces)

def valid_channel(prospective_channel):
    return bool(re.match("^[0-9]*$", prospective_channel))


# Banner Art
def banner():
    cprint("               _____ _______     __  ", 'yellow')
    cprint("              / ____|  __ \ \   / /  ", 'yellow')
    cprint("  _ __  _   _| (___ | |__) \ \_/ /   ", 'yellow')
    cprint(" | '_ \| | | |\___ \|  ___/ \   /    ", 'yellow')
    cprint(" | |_) | |_| |____) | |      | |     ", 'yellow')
    cprint(" | .__/ \__, |_____/|_|      |_|     ", 'yellow')
    cprint(" | |     __/ |                       ", 'yellow')
    cprint(" |_|    |___/                        ", 'yellow')
    cprint("-------------------------------------", 'red')
    cprint("[+] Created by: Soups71", 'blue')
    cprint("-------------------------------------", 'red')

# Arguments for the AP scanner
def get_AP_scanner_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--interface',
                        dest='interface', 
                        help='Specify interface to run attack')
                        
    parser.add_argument('-q', 
                    '--quiet', 
                    action='store_true',
                    dest='quiet', 
                    help='Suppresses normal output of the program')
    parser.add_argument('-w', 
                        '--write',
                        dest='write', 
                        help='Saves AP data to file')
    
    parser.set_defaults(quiet = False, write = False, capture_all=False)
    options = parser.parse_args()
    if not valid_filename(options.write):
        parser.error("[-] Filenames may only include letters, numbers, and/or underscores")
    if not valid_interface(options.interface):
        parser.error("[-] The interface you entered was not found to be connected to the system. Please reconnect it or use a different interface")
    return options


# Arguments for the deauth
def get_deauth_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--interface',
                        dest='interface', 
                        help='Specify interface to run attack')
    parser.add_argument('-b',
                        '--BSSID',
                        dest='bssid', 
                        help='MAC address of the AP you want to target')
    parser.add_argument('-dm', 
                        '--dest_mac', 
                        dest='destination_mac', 
                        help='Destination MAC address. Needed for Deauth attack')
    parser.add_argument('-f', 
                        '--forever', 
                        action='store_true',
                        dest='forever', 
                        help='Sets the duration of the deauth attack')
    parser.add_argument('-q', 
                    '--quiet', 
                    action='store_true',
                    dest='quiet', 
                    help='Suppresses normal output of the program')
    parser.add_argument('-c',
                    '--channel',
                    dest='channel', 
                    help="Specific channels you'd like to scan. Format: -c 1")

    parser.set_defaults(quiet = False)
    options = parser.parse_args()
        # Check if target was provided
    if options.bssid == None:
        parser.error("[-] Please specify an BSSID of the AP for deauth attack, use --help for more info.")
    if not valid_channel(options.channel):
        parser.error("[-] Please enter a valid channel")
    if not valid_interface(options.interface):
        parser.error("[-] The interface you entered was not found to be connected to the system. Please reconnect it or use a different interface")
    return options


# Arguments for gathering handshakes
def get_handshake_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--channel',
                        dest='channel', 
                        help="Specific channels you'd like to scan. Format: -c 1,2,3,4")
    parser.add_argument('-e', 
                        '--eapol', 
                        action='store_true',
                        dest='eapol', 
                        help='Used to only capture eapol packets')
    parser.add_argument('-a', 
                        '--all', 
                        action='store_true',
                        dest='all', 
                        help='Capture all the packets that you can.')
    parser.add_argument('-q', 
                        '--quiet', 
                        action='store_true',
                        dest='quiet', 
                        help='Suppresses normal output of the program')
    parser.set_defaults(quiet = False)
    options = parser.parse_args()
        # Check if target was provided
    if options.channel != None:
        options.channel = [each for each in options.channel.split(',')]
    else:
        options.channel = []
    if options.all and options.eapol:
        parser.error("[+] Please select either to capture all the packets or just EAPOL not both")
    if not valid_channel(options.channel):
        parser.error("[-] Please enter a valid channel")
    if not valid_interface(options.interface):
        parser.error("[-] The interface you entered was not found to be connected to the system. Please reconnect it or use a different interface")
    return options
