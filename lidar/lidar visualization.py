import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar

# Set up pygame
pygame.init()
screen = pygame.display.set_mode((320, 240))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

#lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB1"
BAUDRATE = 115200
lidar = RPLidar(None, PORT_NAME, BAUDRATE, timeout=3)

# used to scale data to fit on the screen
max_distance = 0

scan_data = [0] * 360

def process_data(data):
    global max_distance
    for angle in range(360):
        distance = data[angle]
        if distance > 0: # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            screen.set_at(point, pygame.Color(0, 0, 0))
    pygame.display.update()


if __name__ == '__main__':
    try:
        for scan in lidar.iter_scans():
            for _, angle, distance in scan:
                scan_data[min([359, floor(angle)])] = distance
            process_data(scan_data)
    except:
        print("Stopping")
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()