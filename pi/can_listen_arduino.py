import can

# Open the Pi’s CAN channel
bus = can.interface.Bus(channel='can1', bustype='socketcan')

print("Listening for Arduino messages on can0…")
while True:
    msg = bus.recv()        # blocking until a frame arrives
    if msg is None:
        continue

    try:
        # If you know the Arduino’s ID, you can filter it:
        if msg.arbitration_id == 0x12:
            print(f"Got from Arduino: ID=0x{msg.arbitration_id:X}  Data={msg.data.hex().upper()}")
        else:
            # other nodes, if any
            print(f"Other node: ID=0x{msg.arbitration_id:X}  Data={msg.data.hex().upper()}")
    except KeyboardInterrupt:
        print("Stopping CAN listener.")    
        bus.shutdown()
