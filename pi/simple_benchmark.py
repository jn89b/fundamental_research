#!/usr/bin/env python3
import can
import time
import statistics
import argparse

def measure_one_second(bus, timeout=1.0):
    """Count incoming CAN frames over a 1-second period."""
    count = 0
    t_end = time.time() + timeout
    while time.time() < t_end:
        msg = bus.recv(timeout=timeout)
        if msg:
            count += 1
    return count

def main(total_seconds, channel='can0', bitrate=500000, can_id=None):
    # bring up your CAN interface beforehand:
    # sudo ip link set can0 up type can bitrate 500000

    bus = can.interface.Bus(channel=channel, bustype='socketcan', bitrate=bitrate)
    print(f"Measuring for {total_seconds} × 1 s intervals…")

    counts = []
    for i in range(total_seconds):
        cnt = measure_one_second(bus)
        counts.append(cnt)
        print(f"  Interval {i+1:2d}: {cnt} frames")

    mean_fps = statistics.mean(counts)
    std_fps  = statistics.stdev(counts) if total_seconds > 1 else 0.0

    print("\nResults:")
    print(f"  Mean frames/sec: {mean_fps:.2f}")
    print(f"  Std dev frames/sec: {std_fps:.2f}")

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Measure CAN bus frame rate over N seconds and report mean/stddev."
    )
    p.add_argument('-n', '--seconds', type=int, default=10,
                   help="number of 1 s intervals to measure (default: 10)")
    p.add_argument('--channel', type=str, default='can0',
                   help="SocketCAN interface (default: can0)")
    p.add_argument('--bitrate', type=int, default=500000,
                   help="CAN bitrate in bps (default: 500000)")
    args = p.parse_args()

    main(args.seconds, channel=args.channel, bitrate=args.bitrate)
