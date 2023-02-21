#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from kipr import *
from createserial.commands import open_create, close_create, reset_create, create_dd
from createserial.serial import open_serial, close_serial

from createserial.shutdown import shutdown_create_in

claw = 0
wrist = 1
arm = 3

arm_down = 60
arm_up = 500
claw_closed = 1100
claw_open = 300
wrist_down = 500
wrist_up = 20


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create
    # shutdown_create_in(119)


def shutdown():
    close_create()
    close_serial()


def power_on_self_test():
    enable_servos()
    move(arm_up, 1, arm)
    msleep(100)
    move(claw_closed, 5, claw)
    msleep(100)
    move(claw_open, 5, claw)
    msleep(100)
    move(wrist_down, 5, wrist)
    msleep(100)
    move(wrist_up, 5, wrist)
    msleep(100)
    move(arm_down, 10, arm)


# def move_arm_down():
#     enable_servo(port_arm)
#     set_servo_position(port_arm, arm_down)
#
#
# def move_arm_up():
#     enable_servo(port_arm)
#     set_servo_position(port_arm, arm_up)


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
        print("your done")


def main():
    got_to_first_block()
    got_to_analysis_lab1()
    got_to_second_block()
    gotToAnalysisLab2()
    gotTothirdblock()
    gotToAnalysisLab3()
    gotTofourthblock()


def drive(lm, rm, time):
    create_dd(-5 * lm, -5 * rm)
    msleep(time)
    create_dd(0, 0)


def got_to_first_block():
    print('firstblock')
    # turning
    drive(0, 20, 400)
    drive(80, 80, 3000)
    msleep(2000)


def got_to_analysis_lab1():
    print('analysislab1')
    # backing up
    drive(-20, -20, 1000)
    # turning
    drive(-40, 40, 1500)
    # going straight
    drive(40, 40, 2000)
    msleep(2000)


def got_to_second_block():
    print('secondblock')
    # backup
    drive(-40, -40, 500)
    # turning
    drive(30, -30, 790)
    create_dd(-200, -200)
    msleep(850)
    # turning
    drive(80, 0, 950)
    drive(40, 40, 1500)
    msleep(2000)


def gotToAnalysisLab2():
    print('analysislab2')
    # backingup
    drive(-40, -40, 500)
    # turning
    drive(50, -50, 1500)
    # going straight
    drive(40, 40, 1500)
    msleep(2000)


def gotTothirdblock():
    print('thirdblock')
    # backup
    drive(-40, -40, 500)
    # turning
    drive(50, -50, 780)
    # drivestraight
    drive(70, 70, 2200)
    # turning again
    drive(50, 0, 1300)
    # go straight again
    drive(40, 40, 2000)
    msleep(5000)


def gotToAnalysisLab3():
    print("analysislab3")
    # backing up
    drive(-40, -40, 1000)
    # turning
    drive(40, -40, 1000)
    # go straight
    drive(60, 60, 2500)
    # turn again
    drive(40, -40, 600)
    # go straight
    drive(40, 40, 900)
    msleep(2000)


def gotTofourthblock():
    # backup
    drive(-40, -40, 500)


if __name__ == '__main__':
    with CreateConnection():
        main()
