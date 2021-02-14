import os
from time import sleep

class interface:
    def __init__(self, name):
        self.name = name
        self.channel = 1
        self.kill_changer = False
    def set_monitor_mode(self):
        os.system(f"ifconfig {self.name} down")
        os.system(f"iwconfig {self.name} mode monitor")
        os.system(f"ifconfig {self.name} up")
    def kill_changer(self):
        self.kill_changer = True
    def change_channel(self):
        while not self.kill_changer:
            os.system(f"iwconfig {self.name} channel {self.channel}")
            # switch channel from 1 to 14 each 0.5s
            print(f"Current channel: {self.channel}")
            self.channel = self.channel % 14 + 1
            sleep(0.5)