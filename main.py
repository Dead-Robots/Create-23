#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
import time
from actions import init, shutdown, get_red_ring, get_yellow_ring, deliver_yellow_ring, deliver_tall_rings, \
    get_orange_ring, deliver_orange_ring, deliver_red_ring
from camera import is_left_green
from common import ROBOT
# from kipr import push_button, c_button
# import os
# try:
#     from common import ROBOT
# except FileNotFoundError:
#     print("ROBOT COLOR UNIDENTIFIED.\n\nPress the button if the robot is red.\n\nPress 'C' if the robot is green")
#     while not (push_button() or c_button()):
#         pass
#     if push_button():
#         with open(os.path.expanduser("/home/root/Documents/KISS/DRS/RobotID/bin//whoami.txt"), "w+") as file:
#             file.write("RED")
#     else:
#         with open(os.path.expanduser("~/whoami.txt"), "w+") as file:
#             file.write("GREEN")
from common.gyro_movements import gyro_turn_test, straight_drive_distance
from utilities import wait_for_button


def main():
    init()
    left_green = is_left_green()
    print("left is green?", left_green)
    get_red_ring()
    deliver_red_ring()
    get_orange_ring()
    deliver_orange_ring()
    get_yellow_ring()
    deliver_yellow_ring()
    deliver_tall_rings(left_green)
    shutdown()


if __name__ == '__main__':
    print("I am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
