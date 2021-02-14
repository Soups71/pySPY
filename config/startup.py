import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', 
                        '--deauth', 
                        dest='deauth', 
                        action='store_true', 
                        help='Preform deauth attack')
    parser.add_argument('-b',
                        '--BSSID',
                        dest='bssid', 
                        help='MAC address of the AP you want to target')
    parser.add_argument('-dm', 
                        '--dest_mac', 
                        dest='destination_mac', 
                        help='Destination MAC address')
    # parser.add_argument('-v', 
    #                     '--verbose', 
    #                     dest='verbose', 
    #                     action='store_true', 
    #                     help='Print out results as you go')
    parser.set_defaults(verbose=False, deauth = False)
    options = parser.parse_args()
    return options