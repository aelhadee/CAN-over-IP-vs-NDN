import datetime
import os
import cv2
import socket
import struct
import time
from random import randrange

# from Crypto.Cipher import AES  # pip3 install pycryptodome

host = '127.0.0.1'
port = 9990
address = (host, port)
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# s.connect((host, port))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
msgs_matrix = []
# secret_key = b'\x95S)\x93\x93)\xa0\xae\xf8\x9fuY\xec\xec\xdf\xd4]<\xb2\x00Y\xcdr}\x17U/\x1e\xb1\xe62\xac'
# iv = b'\xa7S\x94{\x8c\xdf\x81E\xc5i}j\xa8\r~'
time_sent = []
while True:

    msgs_matrix_bytes = os.urandom(152)
    #     aes_obj = AES.new(secret_key, AES.MODE_OCB, iv)
    #     [encrypted_payload, tag] = aes_obj.encrypt_and_digest(msgs_matrix_bytes)  # the jpg frame + CAN bytes
    #     # jpg image length is not encrypted because it's needed at the RX side since the jpg size is always different
    try:

        #         s.sendall(encrypted_payload + tag)  # length of the jpg + the frame itself + the 200 bytes
        # s.sendall(msgs_matrix_bytes)
        s.sendto(msgs_matrix_bytes, address)
        t = datetime.datetime.now()
        time_sent.append(str(t.strftime("%I:%M:%S:%f %p")))
    except:
        lognamefile_data_sent = user_log_name + "_" + "tcp_packet_tx_" + str(time.time_ns()) + ".txt"
        with open(lognamefile_data_sent, "a") as log1:
            log1.write("TX Clock time" + "\n")
            e = 0
            for i in range(int(len(time_sent))):
                log1.write(str(time_sent[e]) + "\n")
                e += 1
                if e >= int(len(time_sent)):
                    break

            log1.close()
        break

    msgs_matrix = []  # to avoid appending old data
    time.sleep(15 / 1000)
