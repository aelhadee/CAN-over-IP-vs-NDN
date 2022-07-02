#! /bin/bash
modeprob vcan
ip link add dev vcan0 type vcan
ip link add dev vcan1 type vcan
ip link add dev vcan2 type vcan

ip link set vcan0 # mtu not specified since it's a standard can bus
ip link set vcan1 mtu 72 # to support CAN FD payload
ip link set vcan2 mtu 72 # optional

ip link set dev vcan0 up
ip link set dev vcan1 up
ip link set dev vcan2 up #optional
nfdc strategy set /trailer/ECU/CAN /localhost/nfd/strategy/multicast
