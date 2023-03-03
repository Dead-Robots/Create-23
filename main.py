#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from kipr import *
from kipr import push_button
from createserial.commands import open_create, close_create, reset_create, create_dd
from createserial.serial import open_serial, close_serial
from common import ROBOT

from createserial.shutdown import shutdown_create_in

CLAW = 0
WRIST = 1
ARM = 3

ARM_DOWN = 150
ARM_UP = 1000
CLAW_CLOSED = 1000
CLAW_OPEN = 200
WRIST_DOWN = 500
ARM_CUBE1 = 760
WRIST_UP = 0
ARM_FIRST_CUBE = 680
WRIST_CUBE1 = 160
ARM_HIGH = 1400
WRIST_HIGH = 1270
ARM_CUBE2 = 600
WRIST_CUBE2 = 600


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create
    # shutdown_create_in(119)


def shutdown():
    move(ARM_DOWN, 1, ARM)
    msleep(100)
    move(WRIST_UP, 1, WRIST)
    msleep(100)
    move(CLAW_OPEN, 1, CLAW)
    msleep(1000)
    disable_servos()

def power_on_self_test():
    enable_servos()
    move(ARM_UP, 1, ARM)
    msleep(100)
    move(CLAW_CLOSED, 5, CLAW)
    msleep(100)
    move(CLAW_OPEN, 3, CLAW)
    msleep(100)
    move(WRIST_DOWN, 3, WRIST)
    msleep(100)
    move(WRIST_UP, 3, WRIST)
    msleep(100)
    move(ARM_DOWN, 2, ARM)
    wait_for_button()


# def move_ARM_DOWN():
#     enable_servo(port_ARM)
#     set_servo_position(port_ARM, ARM_DOWN)
#
#
# def move_ARM_UP():
#     enable_servo(port_ARM)
#     set_servo_position(port_ARM, ARM_UP)


def move(position, time, port):
    enable_servo(port)
    current_pos = get_servo_position(port)
    while current_pos > position:
        current_pos = current_pos - 1
        set_servo_position(port, current_pos)
        msleep(time)
    while current_pos < position:
        current_pos = current_pos + 1
        set_servo_position(port, current_pos)
        msleep(time)
    if current_pos == position:
        print("slaaayyyyy!")


def main():
    power_on_self_test()
    go_to_first_block()
    go_to_analysis_lab1()
    go_to_second_block()
    go_to_third_block()
    wait_for_button()
    ARM_resting()
    shutdown()

    # goToAnalysisLab2()
    # goTothirdblock()
    # goToAnalysisLab3()
    # goTofourthblock()


def drive(lm, rm, time):
    create_dd(-5 * rm, -5 * lm)
    msleep(time)
    create_dd(0, 0)


def go_to_first_block():
    print('first block')
    move(ARM_UP, 1, ARM)
    move(WRIST_CUBE1, 1, WRIST)
    move(CLAW_OPEN, 1, CLAW)

    # turning
    drive(40, 0, 230)
    msleep(100)
    drive(50, 50, 3500)
    msleep(2000)
    #grab cube

    #backing up
    drive(-50, -45, 1000)
    move(WRIST_DOWN, 1, WRIST)
    msleep(1000)
    move(ARM_CUBE1, 1, ARM)
    msleep(1000)
    move(CLAW_CLOSED, 1, CLAW)
    #move(ARM_FIRST_CUBE, 1, ARM)
    msleep(2000)
    move(ARM_UP, 1, ARM)
    msleep(1000)


def go_to_analysis_lab1():
    print('analysis lab1')
    #backing up
    drive(-25, -25, 500)
    #rotate
    drive(30, -30, 1700)
    msleep(500)
    drive(25, 25, 500)
    msleep(500)
    put_block()


def put_block():
    move(WRIST_UP, 1, WRIST)
    msleep(100)
    move(ARM_DOWN, 1, ARM)
    msleep(100)
    move(CLAW_OPEN, 1, CLAW)
    msleep(1000)


def go_to_second_block():
    print('second block')
    drive(-25, -25, 750)
    move(1800, 1, ARM)
    msleep(500)
    drive(0, 40, 700)
    drive(40, 40, 2250)
    move(ARM_HIGH, 1, ARM)
    drive(-40, 40, 925)
    move(WRIST_HIGH, 1, WRIST)
    msleep(500)
    drive(40, 40, 850)
    msleep(100)
    move(CLAW_CLOSED, 1, CLAW)
    msleep(100)
    move(WRIST_UP, 1, WRIST)
    msleep(100)
    drive(-40, 40, 1750)
    drive(20, 20, 500)
    # place block
    move(WRIST_CUBE2, 1, WRIST)
    move(ARM_CUBE2, 1, ARM)
    move(CLAW_OPEN, 1, CLAW)
    # grab cube


# def go_to_analysis_lab2():
#     print('analysis lab2')
#     # backingup
#     drive(-40, -40, 500)
#     # turning
#     drive(-50, 50, 1500)
#     # going straight
#     drive(40, 40, 1500)
#     msleep(2000)


def go_to_third_block():
    print('third block')
    # backup
    drive(-40, -40, 500)

    # turning
    # drive(-50, 50, 780)
    #
    # # drivestraight
    # drive(70, 70, 2200)
    #
    # # turning again
    # drive(0, 50, 1300)
    #
    # # go straight again
    # drive(40, 40, 2000)
    # msleep(5000)


def go_to_analysis_lab_3():
    print("analysis lab3")
    # backing up
    drive(-40, -40, 1000)
    # turning
    drive(-40, 40, 1000)
    # go straight
    drive(60, 60, 2500)
    # turn again
    drive(-40, 40, 600)
    # go straight
    drive(40, 40, 900)
    msleep(2000)


def go_to_fourth_block():
    # backup
    drive(-40, -40, 500)



def ARM_resting():
    #wait_for_button()
    move(CLAW_OPEN, 3, CLAW)
    move(WRIST_UP, 3, WRIST)
    move(ARM_DOWN, 3, ARM)


def wait_for_button():
    print("Push. The. BUTTON.")
    while not push_button():
        pass


if __name__ == '__main__':
    if ROBOT.is_yellow:
        print("i am yellow")
    with CreateConnection():
        main()
    shutdown()
