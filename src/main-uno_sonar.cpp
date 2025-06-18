#!/usr/bin/env python3
import can
import csv
import datetime
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
    # allow clean exit on Ctrl+C
    signal.signal(signal.SIGINT, handle_sigint)

    # Make sure can0 is up:
    #   sudo ip link set can0 up type can bitrate 500000

    bus = can.interface.Bus(
        channel=CAN_CHANNEL,
        bustype='socketcan',
        bitrate=CAN_BITRATE
    )
    print(f"Listening for ID 0x{SONAR_CAN_ID:02X} on {CAN_CHANNEL}…")

    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['iso_timestamp', 'epoch_sec', 'distance_cm'])

        while running:
            msg = bus.recv(timeout=1.0)
            if msg is None:
                continue

            if msg.arbitration_id == SONAR_CAN_ID and len(msg.data) >= 1:
                # 1) extract the Arduino’s one-byte payload
                dist_mm = msg.data[0]       # uint8_t(dist_cm*10)
                distance_cm = dist_mm / 10.0

                # 2) two forms of timestamp
                ts_epoch = msg.timestamp     # float seconds since Unix epoch
                ts_iso   = datetime.datetime.fromtimestamp(ts_epoch)\
                                            .isoformat(sep=' ', timespec='milliseconds')

                # 3) write to CSV and flush
                writer.writerow([ts_iso, f"{ts_epoch:.6f}", f"{distance_cm:.1f}"])
                csvfile.flush()

                # 4) feedback on console
                print(f"{ts_iso} | {distance_cm:.1f} cm")

    print("Stopped.")

if __name__ == '__main__':
    main()
