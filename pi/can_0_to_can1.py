#!/usr/bin/env python3
import can

# open both interfaces
bus0 = can.interface.Bus(channel='can0', bustype='socketcan')
bus1 = can.interface.Bus(channel='can1', bustype='socketcan')

print("Forwarding from can0 → can1. Press Ctrl+C to stop.")
try:
    for msg in bus0:  # blocks until a frame arrives on can0
        try:
            bus1.send(msg)
        except can.CanError as e:
            print(f"[can0→can1] Send failed: {e}")
except KeyboardInterrupt:
    print("\nStopping can0→can1 bridge.")
