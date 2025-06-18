#https://raspberrypi.stackexchange.com/questions/137509/can-bus-from-raspberry-pi3-to-arduino-nano
sudo ifconfig can0 down ; sudo ifconfig can1 down
sudo ip link set can0 type can bitrate 500000 ; sudo ip link set can1 type can bitrate 500000
sudo ifconfig can0 txqueuelen 65536 ; sudo ifconfig can1 txqueuelen 65536
sudo ifconfig can0 up ; sudo ifconfig can1 up