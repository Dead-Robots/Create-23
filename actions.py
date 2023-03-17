from kipr import msleep, disable_servos, enable_servos
from createserial.commands import create_dd
import servo
from utilities import wait_for_button, arm_resting
from constants.servos import Claw, Wrist, Arm
from drive import drive
from common import ROBOT


def init():
    enable_servos()
    # shutdown_create_in(119)


def shutdown():
    servo.move(Arm.DOWN, 1)
    servo.move(Wrist.UP, 1)
    servo.move(Claw.OPEN, 1)
    msleep(1000)
    disable_servos()


def power_on_self_test():
    enable_servos()
    servo.move(Arm.UP, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Wrist.UP, 1)
    servo.move(Wrist.DOWN, 1)
    servo.move(Arm.DOWN, 1)
    servo.move(Claw.OPEN, 1)
    wait_for_button()


def go_to_first_cube():
    print('first block')

    drive(40, 0, 230)
    msleep(100)
    servo.move(Arm.HIGHEST, 1)
    servo.move(Wrist.CUBE1, 1)
    servo.move(Claw.OPEN, 1)

    # drive(50, 50, 2000)
    ROBOT.run(drive, red=(50, 50, 2000), yellow=(50, 50, 2000))
    msleep(100)
    drive(-40, 40, 900)
    msleep(100)
    # first square up
    drive(40, 40, 1300)
    msleep(100)
    drive(-40, -40, 1200)
    msleep(100)
    drive(40, -40, 850)
    msleep(100)
    # second square up
    drive(50, 50, 1500)
    msleep(500)
    # grab cube
    # backing up
    drive(-50, -45, 900)
    servo.move(Wrist.CUBE1, 1)
    servo.move(Arm.CUBE1, 1)
    msleep(1000)
    servo.move(Claw.CLOSED, 1)
    msleep(2000)
    servo.move(Arm.UP, 1)
    msleep(1000)


def go_to_analysis_lab1():
    print('analysis lab1')
    # backing up
    drive(-25, -25, 700)
    msleep(200)
    # rotate
    drive(30, -30, 1800)
    msleep(500)
    #drive(-25, -25, 250)
    put_block()


def put_block():
    servo.move(Wrist.DOWN, 1)
    servo.move(Arm.CUBE1_DOWN, 1)
    servo.move(Claw.OPEN, 1)
    msleep(1000)


def go_to_second_cube():
    print('second block')
    # backing up away from 1st cube
    drive(-25, -25, 750)
    msleep(100)
    # arm up
    servo.move(Arm.HIGHEST, 1)
    # turning
    drive(0, 40, 1000)
    msleep(100)
    # going straight
    drive(40, 40, 2050)
    msleep(100)

    # turn towards 2nd cube
    drive(-40, 40, 750)
    msleep(100)
    # square up
    drive(50, 50, 1500)
    msleep(2000)
    # grab cube
    # backing up
    drive(-50, -45, 800)
    # place wrist and arm
    servo.move(Arm.HIGHEST, 1)
    servo.move(Wrist.CUBE2, 1)
    drive(40, 40, 800)
    msleep(500)
    # grab cube
    servo.move(Claw.CLOSED, 1)
    servo.move(Wrist.HIGH, 1)


def go_to_analysis_lab2():
    print('analysis lab2')
    drive(-40, -40, 500)
    # turning
    drive(-40, 40, 1700)
    msleep(100)
    drive(40, 40, 400)
    # place block
    servo.move(Wrist.CUBE2_DOWN, 1)
    servo.move(Arm.CUBE2_DOWN, 2)
    servo.move(Claw.OPEN, 1)
    # grab cube


def go_to_third_cube():
    print('third block')
    # backup
    drive(-40, -40, 500)
    msleep(100)
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    drive(-40, 40, 1100)
    msleep(100)
    drive(54, 50, 2750)
    msleep(100)
    drive(0, 40, 2000)
    msleep(100)
    drive(40, 40, 500)
    # backing up
    drive(-50, -45, 1000)
    # place wrist and arm
    servo.move(Arm.HIGH, 1)
    servo.move(Wrist.HIGH, 1)
    drive(40, 40, 750)
    msleep(500)
    # turning
    # drive(-50, 50, 780)
    #
    # # drive straight
    # drive(70, 70, 2200)
    #
    # # turning again
    # drive(0, 50, 1300)
    #
    # # go straight again
    # drive(40, 40, 2000)
    # msleep(5000)


def go_to_analysis_lab_3():
    print("analysis lab 3")
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
