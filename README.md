# pySPY 
### Version_1.2
![Banner Art](images/banner.png)
## Backstory:
So long story short I kinda hate aircrack-ng. Also I want to make a wifi-Kracken. I didn't feel as though aircrack suite had the same usability that I was looking for so I decided to write my own utility in python. For the actual cracking of handshakes aircrack is still needed but this suite acts in place of airodump, airplay.

## Current offerings
At the moment there are three scripts:
* `apSPY.py`
    * Finds the various AP within radio ear shot
* `deauthenticate.py`
    * Deauthenticates users from the Access point
* `get_handshakes.py`
    * Gets WPA/WPA2 handshakes on the specific channel
    * Collects wifi packets


## Access point monitoring
```
usage: apSPY.py [-h] [-i INTERFACE] [-freq FREQUENCY] [-q] [-w WRITE]

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Specify interface to run attack
  -freq FREQUENCY, --frequency FREQUENCY
                        Specify frequency to run attack: 2 for 2.4 ghz or 5 for 5 ghz
  -q, --quiet           Suppresses normal output of the program
  -w WRITE, --write WRITE
                        Saves AP data to file
```

## Deauthentication 
```
usage: deauthenticate.py [-h] [-i INTERFACE] [-b BSSID] [-dm DESTINATION_MAC] [-freq FREQUENCY] [-f] [-q] [-c CHANNEL]

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Specify interface to run attack
  -b BSSID, --BSSID BSSID
                        MAC address of the AP you want to target
  -dm DESTINATION_MAC, --dest_mac DESTINATION_MAC
                        Destination MAC address. Needed to deauth specific device
  -freq FREQUENCY, --frequency FREQUENCY
                        Specify frequency to run attack: 2 for 2.4 ghz or 5 for 5 ghz
  -f, --forever         Sets the duration of the deauth attack
  -q, --quiet           Suppresses normal output of the program
  -c CHANNEL, --channel CHANNEL
                        Specific channels you'd like to scan. Format: -c 1
```

## Collect Wireless handshakes
```
usage: get_handshakes.py [-h] [-c CHANNEL] [-e] [-a] [-freq FREQUENCY] [-q]

optional arguments:
  -h, --help            show this help message and exit
  -c CHANNEL, --channel CHANNEL
                        Specific channels you'd like to scan. 2.4 or 5 GHz Format: -c 1,2,3,4
  -e, --eapol           Used to only capture eapol packets
  -a, --all             Capture all the packets that you can.
  -freq FREQUENCY, --frequency FREQUENCY
                        Specify frequency to run attack: 2 for 2.4 ghz or 5 for 5 ghz
  -q, --quiet           Suppresses normal output of the program
```

## Disclaimer:
This project is for education and learning. Do NOT use it to attack any networks you do not have explicit permission to test on. I take no responsibility for how you choose to use this. Please consult local laws as to determine the legality of preforming deauthentication attacks and packet sniffing.

Created by: Soups71

