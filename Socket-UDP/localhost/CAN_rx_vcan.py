import datetime
import socket
import time
import cv2
import struct
import numpy as np
from Crypto.Cipher import AES
import can
from can import Message
import matplotlib.pyplot as plt
import os
import pandas as pd

# host = '192.168.137.1''
# host = '10.42.0.1'
host = '127.0.0.1'
port = 9990
address = (host, port)
# tx_ip = '192.168.1.199'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 8)
s.bind(address)
print('listening at', address)
# secret_key = b'\x95S)\x93\x93)\xa0\xae\xf8\x9fuY\xec\xec\xdf\xd4]<\xb2\x00Y\xcdr}\x17U/\x1e\xb1\xe62\xac'
# iv = b'\xa7S\x94{\x8c\xdf\x81E\xc5i}j\xa8\r~'
CAN_bytes = []

# CANFD BUS - 8 Mbits/s
bus1 = can.Bus(channel='vcan0', interface='socketcan')  # pip3 install python-can
bus2_fd = can.Bus(channel='vcan0', interface='socketcan')
start_time = time.time()
start_time_data_received = time.time()
dt_data_received = []
MB = []
while True:
    CAN_bytes = []
    # len of the frame image only
    while len(CAN_bytes) < 152:
        rx_data, _ = s.recvfrom(1024)
        CAN_bytes += rx_data
    print(len(CAN_bytes))
    # CAN msg 1 - Bus 1
    msg1_data = CAN_bytes[0:8]
    msg1 = can.Message(arbitration_id=0xF1, dlc=8, is_extended_id=False, is_fd=False,
                       data=msg1_data)
    bus1.send(msg1)
    # CAN MSG 2 - Bus 1
    msg2_data = CAN_bytes[8:16]
    msg2 = can.Message(arbitration_id=0xF2, dlc=8, is_extended_id=False, is_fd=False,
                       data=msg2_data)
    bus1.send(msg2)
    # CAN MSG 3 - Bus 1
    msg3_data = CAN_bytes[16:24]
    msg3 = can.Message(arbitration_id=0xF3, dlc=8, is_extended_id=False, is_fd=False,
                       data=msg3_data)
    bus1.send(msg3)
    # # CAN FD msg 1 - Bus 2
    # msg1_fd_data = CAN_bytes[24:88]
    # msg1_fd = can.Message(arbitration_id=0xC1, dlc=60, is_extended_id=False, is_fd=True,
    #                       data=msg1_fd_data)
    # bus2_fd.send(msg1_fd)
    #
    # # CAN FD msg 2 - Bus 2
    # msg2_fd_data = CAN_bytes[88:88+9]
    # msg2_fd = can.Message(arbitration_id=0xC2, #dlc=64,
    #                       is_extended_id=True, #is_fd=False,
    #                       data=msg2_fd_data)
    # bus2_fd.send(msg2_fd)

    dt_data_received.append((time.time() - start_time_data_received) * 1000)
    print((time.time() - start_time_data_received)*1e6, 'nano seconds')
    start_time_data_received = time.time()
    if (time.time() - start_time) >= (10 * 60):
        print(dt_data_received)
        logfilename_tcp_rx = "CAN_rx_dt_" + str(time.time_ns()) + ".log"
        with open(logfilename_tcp_rx, "a") as log1:
            log1.write("CAN_RX_Delta_time" + "\n")
            for ii in range(1, int(len(dt_data_received))):
                log1.write(str(dt_data_received[ii]) + "\n")
            log1.close()
        frames_plt = list(range(1, len(dt_data_received)))
        plt.figure(figsize=(10, 8))
        plt.subplot(1, 2, 1)
        plt.scatter(frames_plt, dt_data_received[1:])
        plt.xlabel('NDN Data Packet Number')
        plt.ylabel('Delta time (in ms): Received CAN bytes over NDN Data Packet')

        plt.subplot(1, 2, 2)
        plt.boxplot(dt_data_received[1:])
        plt.savefig("CAN_dt_data_tx_box_" + str(time.time_ns()) + ".png")
        print("Data RX Ended...going to sleep")
        dt_data_received_pd = pd.DataFrame(dt_data_received[1:])
        logfilename_CAN_rx_summ = "CAN_rx_dt_summary" + str(time.time_ns()) + ".log"
        with open(logfilename_CAN_rx_summ, "a") as log2:
            log2.write("CAN_RX_dt_summary" + "\n")
            log2.write(str(dt_data_received_pd.describe()) + "\n")
            log2.close()
        print(dt_data_received_pd.describe())
        print(MB, 'bytes')
        print(MB / 1000000, 'MB')
        time.sleep(60 * 60)
