#! /bin/bash
modeprob vcan
ip link add dev vcan0 type vcan
ip link add dev vcan1 type vcan
ip link add dev vcan2 type vcan

ip link set vcan0 mtu 72
ip link set vcan1 mtu 72
ip link set vcan2 mtu 72

ip link set dev vcan0 up
ip link set dev vcan1 up
ip link set dev vcan2 up
nfdc strategy set /trailer/ECU/CAN /localhost/nfd/strategy/multicast
