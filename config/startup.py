import argparse

def get_deauth_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', 
                        '--deauth', 
                        dest='deauth', 
                        action='store_true', 
                        help='Preform deauth attack')
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
                        dest='forever', 
                        help='Sets the duration of the deauth attack')

    # parser.add_argument('-v', 
    #                     '--verbose', 
    #                     dest='verbose', 
    #                     action='store_true', 
    #                     help='Print out results as you go')
    parser.set_defaults(verbose=False, deauth = False)
    options = parser.parse_args()
        # Check if target was provided
    if options.deauth and not options.bssid:
        parser.error("[-] Please specify an BSSID mac for deauth attack, use --help for more info.")


    return options