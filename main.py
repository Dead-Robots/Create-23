#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from kipr import msleep

import servo
from actions import init, shutdown, get_red_ring, \
    get_yellow_ring, deliver_yellow_ring, green_ring_left, get_orange_ring, deliver_orange_ring, blue_ring_left, \
    blue_ring_right, deliver_red_ring
from common import ROBOT
from common.gyro_movements import gyro_turn_test, straight_drive_distance
from drive import square_up_black


def main():
    init()
    get_red_ring()
    deliver_red_ring()
    get_orange_ring()
    deliver_orange_ring()
    # get_yellow_ring()
    # deliver_yellow_ring()
    # green_ring_left()
    # blue_ring_right()
    shutdown()


if __name__ == '__main__':
    print("I am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
