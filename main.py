#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from common.utilities import wait_for_button
from actions import init, shutdown, go_to_first_cube, go_to_analysis_lab1, go_to_second_cube, go_to_third_cube, \
    arm_resting, power_on_self_test
from common import ROBOT


def main():
    init()
    power_on_self_test()
    go_to_first_cube()
    # go_to_analysis_lab1()
    # go_to_second_cube()
    # go_to_third_cube()
    # wait_for_button()
    arm_resting()
    # shutdown()

    # go_to_analysis_lab2()
    # go_to_third_cube()
    # go_to_analysis_lab3()
    # got_to_fourth_block()


if __name__ == '__main__':
    print("i am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
