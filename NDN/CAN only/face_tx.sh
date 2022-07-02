#! /bin/bash
nfdc strategy set /trailer/ECU/CAN /localhost/nfd/strategy/multicast
nfdc face create udp://192.168.10.11
nfdc route add /trailer/serial/buses udp://192.168.10.11

