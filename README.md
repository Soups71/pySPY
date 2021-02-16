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

