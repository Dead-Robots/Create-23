#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from common.utilities import wait_for_button

from actions import shutdown, got_to_first_block, got_to_analysis_lab1, got_to_second_block, arm_resting
from common import ROBOT

# shutdown_position = 75  (what is this?)

arm_down = 150
arm_up = 1000
arm_first_cube = 680
arm_2 = 820
arm_high = 1400

claw_closed = 950
claw_open = 600
claw_first_cube1 = 300
claw_closed_cube1 = 900

wrist_down = 500
wrist_up = 0
first_wrist = 160
wrist_2 = 700
wrist_high = 1270


# def move_arm_down():
#     enable_servo(port_arm)
#     set_servo_position(port_arm, arm_down)
#
#
# def move_arm_up():
#     enable_servo(port_arm)
#     set_servo_position(port_arm, arm_up)


def main():
    # power_on_self_test()
    got_to_first_block()
    got_to_analysis_lab1()
    got_to_second_block()
    wait_for_button()
    arm_resting()
    shutdown()

    # gotToAnalysisLab2()
    # gotTothirdblock()
    # gotToAnalysisLab3()
    # gotTofourthblock()


if __name__ == '__main__':
    if ROBOT.is_yellow:
        print("i am yellow")
    with CreateConnection():
        main()
    shutdown()
