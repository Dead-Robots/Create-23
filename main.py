#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from kipr import *
from kipr import push_button
from createserial.commands import open_create, close_create, reset_create, create_dd
from createserial.serial import open_serial, close_serial
from common import ROBOT

from createserial.shutdown import shutdown_create_in

claw = 0
wrist = 1
arm = 3

arm_down = 150
arm_up = 1000
claw_closed = 950
claw_open = 600
wrist_down = 500
wrist_up = 0
arm_first_cube = 680
shutdown_position = 75
claw_first_cube1 = 300
first_wrist = 160
arm_2 = 820
wrist_2 = 700
claw_closed_cube1 = 900
arm_high = 1400
wrist_high = 1270

def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create
    # shutdown_create_in(119)


def shutdown():
    move(arm_down, 1, arm)
    msleep(100)
    move(wrist_up, 1, wrist)
    msleep(100)
    move(claw_open, 1, claw)
    msleep(1000)
    disable_servos()

def power_on_self_test():
    enable_servos()
    move(arm_up, 1, arm)
    msleep(100)
    move(claw_closed, 5, claw)
    msleep(100)
    move(claw_open, 3, claw)
    msleep(100)
    move(wrist_down, 3, wrist)
    msleep(100)
    move(wrist_up, 3, wrist)
    msleep(100)
    move(arm_down, 2, arm)


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
        print("slaaayyyyy!")


def main():
    #power_on_self_test()
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


def drive(lm, rm, time):
    create_dd(-5 * rm, -5 * lm)
    msleep(time)
    create_dd(0, 0)


def got_to_first_block():
    print('first block')
    move(arm_up, 1, arm)
    move(first_wrist, 1, wrist)
    move(claw_first_cube1, 1, claw)

    # turning
    drive(40, 0, 230)
    msleep(100)
    drive(50, 50, 3500)
    msleep(2000)
    #grab cube

    #backing up
    drive(-50, -45, 1000)
    move(wrist_2, 1, wrist)
    msleep(1000)
    move(arm_2, 1, arm)
    msleep(1000)
    move(claw_closed_cube1, 1, claw)
    #move(arm_first_cube, 1, arm)
    msleep(2000)
    move(arm_up, 1, arm)
    msleep(1000)



def got_to_analysis_lab1():
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
    move(wrist_up, 1, wrist)
    msleep(100)
    move(arm_down, 1, arm)
    msleep(100)
    move(300, 1, claw)
    msleep(1000)


def got_to_second_block():
    print('second block')
    drive(-25, -25, 750)
    move(1800, 1, arm)
    msleep(500)
    drive(0, 40, 700)
    drive(40, 40, 2250)
    move(arm_high, 1, arm)
    move(wrist_high, 1, wrist)
    drive(-40, 40, 925)
    msleep(500)
    drive(40, 40, 750)
    msleep(100)
    move(claw_closed_cube1, 1, claw)
    msleep(100)
    move(wrist_up, 1, wrist)
    msleep(100)
    drive(-40, 40, 1800)
    move(600, 1, wrist)
    move(600, 1, arm)
    move(claw_open, 1, claw)
    # grab cube


    # backup
    # drive(-40, -40, 500)
    # # turning
    # drive(30, -30, 790)
    # create_dd(-200, -200)
    # msleep(850)
    # # turning
    # drive(80, 0, 950)
    # drive(40, 40, 1500)
    # msleep(2000)


def got_to_analysis_lab2():
    print('analysis lab2')
    # backingup
    drive(-40, -40, 500)
    # turning
    drive(-50, 50, 1500)
    # going straight
    drive(40, 40, 1500)
    msleep(2000)


def got_to_third_block():
    print('third block')
    # backup
    drive(-40, -40, 500)
    # turning
    drive(-50, 50, 780)
    # drivestraight
    drive(70, 70, 2200)
    # turning again
    drive(0, 50, 1300)
    # go straight again
    drive(40, 40, 2000)
    msleep(5000)


def got_to_analysis_lab_3():
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


def got_to_fourth_block():
    # backup
    drive(-40, -40, 500)



def arm_resting():
    #wait_for_button()
    move(claw_open, 3, claw)
    move(wrist_up, 3, wrist)
    move(arm_down, 3, arm)


def wait_for_button():
    while not push_button():
        pass


if __name__ == '__main__':
    if ROBOT.is_yellow:
        print("i am yellow")
    with CreateConnection():
        main()
    shutdown()
