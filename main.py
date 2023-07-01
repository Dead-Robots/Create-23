#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from kipr import msleep, motor_power
import time
import servo
from actions import init, shutdown, get_red_ring, \
    get_yellow_ring, deliver_yellow_ring, deliver_tall_rings, get_orange_ring, deliver_orange_ring, deliver_red_ring
from common import ROBOT
from common.gyro_movements import gyro_turn_test, straight_drive_distance
from drive import square_up_black
from utilities import wait_for_button


def main():
    init()
    left_green = True
    start_time = time.time()
    get_red_ring()
    deliver_red_ring()
    get_orange_ring()
    deliver_orange_ring()
    get_yellow_ring()
    deliver_yellow_ring()
    deliver_tall_rings(left_green)
    print(str(time.time() - start_time) + " seconds elapsed.")
    shutdown()


if __name__ == '__main__':
    print("I am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
