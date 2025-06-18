import can

# bring up your interface first in the shell:
# sudo ip link set can0 up type can bitrate 500000
# https://python-can.readthedocs.io/en/stable/

# then in Python:
bus = can.interface.Bus(channel='can0', bustype='socketcan')

print("Listening on CAN interface can0…")
try:
    for msg in bus:
        print(f"ID: {msg.arbitration_id:03X}  Data: {msg.data.hex().upper()}  Timestamp: {msg.timestamp:.6f}")
except KeyboardInterrupt:
    bus.shutdown()
    print("Stopped.")
