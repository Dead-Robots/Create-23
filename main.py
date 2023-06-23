#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection

import servo
from actions import init, shutdown, get_red_ring, deliver_red_ring, \
    get_yellow_ring, deliver_yellow_ring, green_ring_left, get_orange_ring, deliver_orange_ring, blue_ring_left,\
    blue_ring_right
from common import ROBOT
from common.gyro_movements import gyro_turn_test
from constants.servos import Arm
from utilities import wait_for_button


def main():
    init()
    servo.move(Arm.STRAIGHT_UP, 1)
    gyro_turn_test(60, -60, 90, 4)
    exit(0)
    # get_red_ring()
    # deliver_red_ring()
    # get_orange_ring()
    # deliver_orange_ring()
    # get_yellow_ring()
    # deliver_yellow_ring()
    # green_ring_left()
    # blue_ring_right()
    # get_first_ring()
    # move_rings()

    # shutdown()


if __name__ == '__main__':
    print("I am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
