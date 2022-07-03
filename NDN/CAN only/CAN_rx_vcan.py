# -----------------------------------------------------------------------------
# Copyright (C) 2019-2020 The python-ndn authors
#
# This file is part of python-ndn.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
import logging
import time

import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name, Component, InterestParam
import pandas as pd
import matplotlib.pyplot as plt
import can

global start_time, start_time_data_received, dt_data_received, MB
start_time = time.time()
start_time_data_received = time.time()
dt_data_received = []
MB = []
logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

app = NDNApp()

bus1 = can.Bus(channel='vcan0', interface='socketcan')  # pip3 install python-can
bus2_fd = can.Bus(channel='vcan0', interface='socketcan')


# bus3_fd = can.Bus(channel='vcan2', interface='socketcan', fd= True)
async def main():
    global start_time, start_time_data_received, dt_data_received
    MB = 0

    while True:
        try:
            timestamp = ndn.utils.timestamp()
            name = Name.from_str('/trailer/ECU/CAN') + [Component.from_timestamp(timestamp)]
            data_name, meta_info, content = await app.express_interest(
                name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            CAN_bytes = bytes(content)

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
<<<<<<< HEAD
            msg2_fd_data = CAN_bytes[88:88+10]
            msg2_fd = can.Message(arbitration_id=0xC2, #dlc=64,
                                  is_extended_id=False, is_fd=False,
                                  data=msg2_fd_data)
            bus2_fd.send(msg2_fd)
=======
            # msg2_fd_data = CAN_bytes[88:88+9]
            # msg2_fd = can.Message(arbitration_id=0xC2, #dlc=64,
            #                       is_extended_id=True, #is_fd=False,
            #                       data=msg2_fd_data)
            # bus2_fd.send(msg2_fd)
>>>>>>> c74461d79b83257087b74e85493dd51d4eaf0afb

            MB += len(content)

        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')

        dt_data_received.append((time.time() - start_time_data_received) * 1000)
        start_time_data_received = time.time()
        if (time.time() - start_time) >= (1 * 60):
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
            app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())

