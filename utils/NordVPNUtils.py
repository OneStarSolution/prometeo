import time
import socket

from nordvpn_switcher import initialize_VPN, rotate_VPN

# [1] save settings file as a variable

# this will guide you through a step-by-step guide, including a help-menu with connection options
instructions = initialize_VPN(
    save=1, area_input=['random regions united states 3'])

for i in range(3):
    rotate_VPN(instructions)  # refer to the instructions variable here
    time.sleep(10)
    print(socket.gethostbyname(socket.gethostname()))
