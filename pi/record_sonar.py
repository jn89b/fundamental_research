#!/usr/bin/env python3
import can
import csv
import signal
import sys

# ——— CONFIG ———
CAN_CHANNEL   = 'can0'     # your SocketCAN interface
CAN_BITRATE   = 500000     # must match Arduino (500 kbps)
SONAR_CAN_ID  = 0x12       # as used in sendDistanceCAN()
OUTPUT_CSV    = 'sonar_log.csv'
# —————————

running = True

def handle_sigint(sig, frame):
    global running
    running = False

def main():
    signal.signal(signal.SIGINT, handle_sigint)

    # Make sure can0 is up (run once beforehand):
    # sudo ip link set can0 up type can bitrate 500000

    bus = can.interface.Bus(
        channel=CAN_CHANNEL,
        bustype='socketcan',
        bitrate=CAN_BITRATE
    )
    print(f"Listening for ID 0x{SONAR_CAN_ID:02X} on {CAN_CHANNEL}…")

    start_ts = None

    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time_ms', 'distance_cm'])

        while running:
            msg = bus.recv(timeout=1.0)
            if msg is None:
                continue

            if msg.arbitration_id == SONAR_CAN_ID and len(msg.data) >= 1:
                # 1) extract the Arduino’s payload
                dist_mm = msg.data[0]       # uint8_t(dist_cm*10)
                distance_cm = dist_mm / 10.0

                # 2) initialize start timestamp
                if start_ts is None:
                    start_ts = msg.timestamp

                # 3) compute elapsed milliseconds
                elapsed_ms = int((msg.timestamp - start_ts) * 1000)

                # 4) write and flush
                writer.writerow([elapsed_ms, f"{distance_cm:.1f}"])
                csvfile.flush()

                # 5) console feedback
                print(f"{elapsed_ms:6d} ms | {distance_cm:.1f} cm")

    print("Stopped.")

if __name__ == '__main__':
    main()
