#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from actions import init, shutdown, go_to_first_cube, power_on_self_test, go_to_analysis_lab1, go_to_second_cube, \
    go_to_analysis_lab2, go_to_third_cube, go_to_analysis_lab3, go_to_fourth_block, go_to_analysis_lab4, \
    start_position, end_position, test_turn_for_gyro
from common import ROBOT
from utilities import wait_for_button


def main():
    test_turn_for_gyro()
    exit(0)
    init()
    start_position()
    # drive_straight_test()
    # power_on_self_test()
    go_to_first_cube()
    go_to_analysis_lab1()
    go_to_second_cube()
    go_to_analysis_lab2()
    go_to_third_cube()
    go_to_analysis_lab3()
    go_to_fourth_block()
    go_to_analysis_lab4()
    end_position()

    # shutdown()


if __name__ == '__main__':
    print("i am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
