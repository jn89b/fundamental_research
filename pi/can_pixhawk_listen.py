#!/usr/bin/env python3
import can
import struct
import math

def main():
    # Open the can1 interface
    bus = can.interface.Bus(channel='can1', bustype='socketcan')
    print("Listening on CAN:", bus.channel_info)

    try:
        while True:
            msg = bus.recv()             # blocking read
            if msg is None:
                continue

            # Filter on the ID you used
            if msg.arbitration_id == 0x2:
                # Unpack three big-endian signed shorts; ignore the last two padding bytes
                roll_i, pitch_i, yaw_i = struct.unpack('>hhhxx', msg.data)

                # Scale back to radians
                roll  = roll_i  / 32767.0 * math.pi
                pitch = pitch_i / 32767.0 * math.pi
                yaw   = yaw_i   / 32767.0 * math.pi

                print(f"Decoded → Roll:  {roll:.3f} rad, "
                      f"Pitch: {pitch:.3f} rad, "
                      f"Yaw:   {yaw:.3f} rad")

    except KeyboardInterrupt:
        print("\nInterrupted by user — shutting down CAN bus.")
    finally:
        bus.shutdown()
        print("CAN bus shut down cleanly.")

if __name__ == "__main__":
    main()
