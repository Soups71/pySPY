# pySPY

## Backstory:
So long story short I kinda hate aircrack-ng. Also I want to make a wifi-Kracken. I didn't feel as though aircrack had the same usability that I was looking for so I decided to write my own utility in python.

## Current offerings
At the moment there are two scripts:
* `deauthenticate.py`
    * Deauthenticates users from the Access point
* `get_handshakes.py`
    * Gets WPA/WPA2 handshakes on the specific channel

## Usage
* `sudo python3 deauthenticate.py -b MAC_ADDR -f`
* `sudo python3 get_handshakes.py`

## Disclaimer:
This project is for education and learning. Do NOT use it to attack any networks you do not have explicit permission to test on. I take no responsibility for how you choose to use this. Please consult local laws as to the legality to preform deauthentication attacks and packet sniffing.

Created by: Soups71

