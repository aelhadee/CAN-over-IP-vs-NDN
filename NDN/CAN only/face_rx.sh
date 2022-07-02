#! /bin/bash
# set nfdc strategy with the data name
nfdc strategy set /trailer/ECU/CAN /localhost/nfd/strategy/multicast
# create interface (to the other host)
# nfdc face create udp://<the IP of other device>
# nfdc route add <Name of the group> udp://<other-host>
nfdc face create udp://192.168.10.13
nfdc route add /trailer/serial/buses udp://192.168.10.13