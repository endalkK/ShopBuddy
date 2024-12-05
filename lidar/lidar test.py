# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT
from math import floor
from adafruit_rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB1"
BAUDRATE = 115200
lidar = RPLidar(None, PORT_NAME, BAUDRATE, timeout=3)

# used to scale data to fit on the screen
max_distance = 0

def process_data(data):
    print(data)

scan_data = [0] * 360

try:
    #    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping.")
    lidar.stop()
    lidar.disconnect()

"""for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break
"""
