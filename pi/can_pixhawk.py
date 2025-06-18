#!/usr/bin/env python3
import time
import math
import can
from pymavlink import mavutil

def scale_to_int16(x_rad: float) -> int:
    """Scale x in [-π, +π] into signed 16-bit."""
    max_int = 32767
    return int(max(min(x_rad/math.pi, 1.0), -1.0) * max_int)

def encode_rpy(roll_rad: float, pitch_rad: float, yaw_rad: float) -> bytearray:
    """Pack into 8 bytes: [R_hi,R_lo,P_hi,P_lo,Y_hi,Y_lo,0x00,0x00]."""
    r = scale_to_int16(roll_rad)
    p = scale_to_int16(pitch_rad)
    y = scale_to_int16(yaw_rad)
    return bytearray([
        (r >> 8) & 0xFF, r & 0xFF,
        (p >> 8) & 0xFF, p & 0xFF,
        (y >> 8) & 0xFF, y & 0xFF,
        0x00, 0x00
    ])

# 1) Open MAVLink
mav = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
mav.wait_heartbeat()
print(f"Heartbeat from sys#{mav.target_system} comp#{mav.target_component}")

# 1a) Request higher-rate attitude messages
freq = 30        # desired rate in Hz
dt   = 1.0 / freq
dt_us = int(dt * 1e6)  # interval in microseconds


# (Optional) also request via the STREAM API for broader compatibility
mav.mav.request_data_stream_send(
    mav.target_system,
    mav.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_EXTRA1,  # includes ATTITUDE
    freq,  # Hz
    1      # start
)

# 2) Open SocketCAN
bus = can.interface.Bus(channel='can0', bustype='socketcan')
print(f"CAN bus up on {bus.channel_info}")

try:
    can_id = 0x2
    while True:
        t_frame = time.time()
        # 3) Wait for the next ATTITUDE message
        msg = mav.recv_match(type='ATTITUDE', blocking=True, timeout=0.1)
        if not msg:
            continue

        # 4) Encode & send over CAN
        data = encode_rpy(msg.roll, msg.pitch, msg.yaw)
        frame = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
        try:
            bus.send(frame)
            elapsed = time.time() - t_frame
            # print(f"Sent CAN 0x{can_id:X} {data.hex()}  loop={elapsed:.4f}s")
        except can.CanError:
            print("ERROR: CAN send failed")

        # 7) Throttle precisely to your desired rate
        time.sleep(dt)

except KeyboardInterrupt:
    print("Exiting.")

finally:
    bus.shutdown()
