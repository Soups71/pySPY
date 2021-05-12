#!/bin/bash

sudo apt install git bc bison flex libssl-dev libncurses5-dev
sudo wget https://raw.githubusercontent.com/RPi-Distro/rpi-source/master/rpi-source -O /usr/local/bin/rpi-source && sudo chmod +x /usr/local/bin/rpi-source && /usr/local/bin/rpi-source -q --tag-update
sudo rpi-update
sudo rpi-source
git clone https://github.com/gnab/rtl8812au.git
cd rtl8812au
chmod +x rtl8812au/install.sh
rtl8812au/install.sh