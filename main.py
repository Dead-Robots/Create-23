#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from actions import init, shutdown, get_red_ring, deliver_red_ring, \
    get_yellow_ring, deliver_yellow_ring, green_ring_left, get_orange_ring, deliver_orange_ring, blue_ring_left,\
    blue_ring_right
from common import ROBOT
from utilities import wait_for_button


def main():
    init()
    wait_for_button()
    # calibrate_straight_drive_distance(11.5, direction=-1, speed=20)
    # exit(0)
    get_red_ring()
    deliver_red_ring()
    get_orange_ring()
    deliver_orange_ring()
    get_yellow_ring()
    deliver_yellow_ring()
    green_ring_left()
    blue_ring_right()
    # get_first_ring()
    # move_rings()

    shutdown()


if __name__ == '__main__':
    print("I am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
