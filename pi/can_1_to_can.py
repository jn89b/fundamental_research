#!/usr/bin/env python3
import can

# open both interfaces
bus1 = can.interface.Bus(channel='can1', bustype='socketcan')
bus0 = can.interface.Bus(channel='can0', bustype='socketcan')

print("Forwarding from can1 → can0. Press Ctrl+C to stop.")
try:
    for msg in bus1:  # blocks until a frame arrives on can1
        try:
            bus0.send(msg)
        except can.CanError as e:
            print(f"[can1→can0] Send failed: {e}")
except KeyboardInterrupt:
    print("\nStopping can1→can0 bridge.")
