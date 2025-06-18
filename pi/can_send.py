#!/usr/bin/env python

"""
This example shows how sending a single message works.
"""

import can
import time 

def send_one():
    """Sends a single message."""

    # this uses the default configuration (for example from the config file)
    # see https://python-can.readthedocs.io/en/stable/configuration.html
    with can.Bus(channel='can0', bustype='socketcan') as bus:
        # Using specific buses works similar:
        # bus = can.Bus(interface='socketcan', channel='vcan0', bitrate=250000)
        # bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        # bus = can.Bus(interface='ixxat', channel=0, bitrate=250000)
        # bus = can.Bus(interface='vector', app_name='CANalyzer', channel=0, bitrate=250000)
        # ...

        # msg = can.Message(
        #     arbitration_id=0x123,
        #     data=[0x11, 0x22, 0x33, 0x44],
        #     is_extended_id=False
        # )

        msg = can.Message(
            arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True
        )

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            bus.shutdown()
            print("Message NOT sent")


if __name__ == "__main__":
    
    for i in range(100):
        send_one()
        time.sleep(0.001)