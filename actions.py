from kipr import msleep, disable_servos, enable_servos
from createserial.commands import create_dd
import servo
from utilities import wait_for_button, arm_resting
from constants.servos import Claw, Wrist, Arm
from drive import drive, untimed_drive, square_up_tophats, square_up_white
from common import ROBOT
from sensors import on_black_left


def init():
    enable_servos()
    servo.move(Wrist.DOWN, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.DOWN, 1)
    # shutdown_create_in(119)


def shutdown():
    servo.move(Arm.START, 1)
    servo.move(Wrist.START, 1)
    servo.move(Claw.OPEN, 1)
    msleep(1000)
    disable_servos()

# start box position
def start_position():
    servo.move(Arm.START, 1)
    servo.move(Wrist.START, 1)
    servo.move(Claw.OPEN, 1)
    wait_for_button()


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


def drive_straight_test():
    square_up_tophats(30, 30)

def go_to_first_cube():
    print('first block')

    drive(40, 0, 230)
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.CUBE1, 0)
    servo.move(Claw.OPEN, 0)

    ROBOT.run(drive, red=(50, 50, 2000), yellow=(60, 60, 2000), blue=(50, 50, 2000))
    ROBOT.run(drive, yellow=(-40, 40, 900), blue=(-40, 40, 1000))
    # first square up
    ROBOT.run(drive, yellow=(40, 40, 1300), blue = (40, 40, 1500))
    ROBOT.run(drive, yellow=(-40, -40, 1250), blue=(-40, -40, 1400))
    drive(40, -40, 850)
    # second square up
    drive(50, 50, 1550)

    # backing up
    ROBOT.run(drive, yellow=(-50, -45, 900), blue=(-50, -50, 1000))
    # grab cube
    servo.move(Wrist.CUBE1, 1)
    servo.move(Arm.CUBE1, 1)
    servo.move(Claw.CLOSED, 1)
    msleep(500)
    servo.move(Arm.UP, 1)


def go_to_analysis_lab1():
    print('analysis lab1')
    # backing up
    drive(-25, -25, 450)
    # rotate towards analysis lab
    drive(40, -40, 800)
    drive(66, 60, 2000)
    # wait_for_button()
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(-25, -25, 400)
    drive(40, -40, 875)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    put_block()
    drive(-40, -40, 500)


def put_block():
    servo.move(Wrist.DOWN, 1)
    servo.move(Arm.CUBE1_DOWN, 1)
    servo.move(Claw.OPEN, 1)
    msleep(1000)


def go_to_second_cube():
    print('second block')
    # arm up
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.UP, 1)
    # rotate 90 degrees right
    drive(40, -40, 950)
    # move forwards
    drive(40, 40, 1100)
    # rotate 90 degrees right
    drive(40, -40, 850)
    # square up
    drive(50, 50, 1600)
    msleep(100)
    # grab cube
    # backing up
    drive(-50, -45, 800)
    # place wrist and arm
    servo.move(Arm.CUBE2, 1)
    servo.move(Wrist.CUBE2, 1, 2)
    drive(40, 40, 800)
    # grab cube
    servo.move(Claw.CLOSED, 1)
    servo.move(Wrist.HIGH, 1)
    drive(-25, -25, 1300)


def go_to_analysis_lab2():
    print('analysis lab2')
    # rotate
    drive(40, -40, 900)
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(0, 0, 0)
    untimed_drive(-10, -10)
    while on_black_left():
        pass
    drive(-25, -25, 300)
    drive(40, -40, 875)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    drive(-25, -25, 650)
    servo.move(Wrist.CUBE2_DOWN, 1)
    servo.move(Arm.CUBE2_DOWN, 2)
    # deliver second log
    servo.move(Claw.OPEN, 1)
    drive(-40, -40, 500)
    servo.move(Arm.HIGHEST, 1)
    drive(25, 25, 500)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)



def go_to_third_cube():
    print('third block')
    # towards cube 3
    drive(42, 40, 2200)
    msleep(100)
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    drive(-40, 40, 850)
    msleep(100)
    drive(50, 50, 1200)
    msleep(100)
    # backing up
    drive(-50, -50, 600)
    # place wrist and arm
    servo.move(Arm.CUBE2, 1)
    servo.move(Wrist.CUBE2, 1, 2)
    drive(40, 40, 800)
    # grab cube
    servo.move(Claw.CLOSED, 1)
    servo.move(Wrist.HIGH, 1)
    drive(-25, -25, 1200)



def go_to_analysis_lab3():
    print("analysis lab 3")
    drive(-25, -25, 900)
    drive(-40, 40, 950)
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(25, 25, 1850)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    drive(-25, -25, 825)
    msleep(100)
    servo.move(Wrist.CUBE3_DOWN, 1)
    msleep(100)
    servo.move(Arm.CUBE3_DOWN, 1)
    msleep(100)
    servo.move(Claw.OPEN, 1)


def go_to_fourth_block():
    drive(-25, -25, 600)
    servo.move(Arm.HIGHEST, 1, 2)
    drive(25, 25, 600)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    drive(42, 40, 4200)
    msleep(100)
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    drive(-40, 40, 850)
    msleep(100)
    drive(50, 50, 1550)

    # backing up
    ROBOT.run(drive, yellow=(-50, -45, 900), blue=(-50, -50, 1000))
    # grab cube
    servo.move(Wrist.CUBE1, 1)
    servo.move(Arm.CUBE1, 1)
    servo.move(Claw.CLOSED, 1)
    msleep(500)
    servo.move(Arm.HIGHEST, 1)
    servo.move(Wrist.HIGH, 1)
    drive(-25, -25, 450)

def go_to_analysis_lab4():
    print("analysis lab 4")
    drive(-40, 40, 950)
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(25, 25, 1850)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    drive(-25, -25, 825)
    msleep(100)
    servo.move(Wrist.CUBE4_DOWN, 1)
    msleep(100)
    servo.move(Arm.CUBE4_DOWN, 1)
    msleep(100)
    servo.move(Claw.OPEN, 1)
    wait_for_button()
