import argparse

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

    parser.set_defaults(deauth = False)
    options = parser.parse_args()
        # Check if target was provided
    if options.deauth and not options.bssid:
        parser.error("[-] Please specify an BSSID mac for deauth attack, use --help for more info.")

    return options
