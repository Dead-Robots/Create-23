from kipr import msleep, disable_servos, enable_servos, enable_servo, get_servo_position, set_servo_position
from createserial.commands import open_create, reset_create, create_dd
from createserial.serial import open_serial, close_serial
from createserial.shutdown import shutdown_create_in
from common import servo
from common.utilities import wait_for_button
from constants.servos import Claw, Wrist, Arm


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()    # Initialize the Create
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
    servo.move(Claw.CLOSED, 5)
    servo.move(Claw.OPEN, 3)
    servo.move(Wrist.DOWN, 3)
    servo.move(Wrist.UP, 3)
    servo.move(Arm.DOWN, 2)
    wait_for_button()


def drive(left_speed, right_speed, duration):
    create_dd(-5 * right_speed, -5 * left_speed)
    msleep(duration)
    create_dd(0, 0)


def go_to_first_cube():
    print('first block')
    servo.move(Arm.UP, 1)
    servo.move(Wrist.CUBE1, 1)
    servo.move(Claw.OPEN, 1)

    # turning
    drive(40, 0, 230)
    msleep(100)
    drive(50, 50, 3500)
    msleep(2000)
    # grab cube

    # backing up
    drive(-50, -45, 1000)
    servo.move(Wrist.DOWN, 1)
    msleep(1000)
    servo. move(Arm.CUBE1, 1)
    msleep(1000)
    servo.move(Claw.CLOSED, 1)
    # move(680, 1, ARM)
    msleep(2000)
    servo.move(Arm.UP, 1)
    msleep(1000)


def go_to_analysis_lab1():
    print('analysis lab1')
    # backing up
    drive(-25, -25, 500)
    # rotate
    drive(30, -30, 1700)
    msleep(500)
    drive(25, 25, 500)
    msleep(500)
    put_block()


def put_block():
    servo.move(Wrist.UP, 1)
    servo.move(Arm.DOWN, 1)
    servo.move(Claw.OPEN, 1)
    msleep(1000)


def go_to_second_cube():
    print('second block')
    drive(-25, -25, 750)
    servo.move(Arm.UNKNOWN, 1)
    drive(0, 40, 700)
    drive(40, 40, 2250)
    servo.move(Arm.HIGH, 1)
    drive(-40, 40, 925)
    servo.move(Wrist.HIGH, 1)
    drive(40, 40, 850)
    servo. move(Claw.CLOSED, 1)
    servo.move(Wrist.UP, 1)
    drive(-40, 40, 1750)
    drive(20, 20, 500)
    # place block
    servo.move(Wrist.CUBE2, 1)
    servo.move(Arm.CUBE2, 1)
    servo.move(Claw.OPEN, 1)
    # grab cube


# def go_to_analysis_lab2():
#     print('analysis lab2')
#     # backing up
#     drive(-40, -40, 500)
#     # turning
#     drive(-50, 50, 1500)
#     # going straight
#     drive(40, 40, 1500)
#     msleep(2000)


def go_to_third_cube():
    print('third block')
    # backup
    drive(-40, -40, 500)

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


def arm_resting():
    # wait_for_button()
    servo.move(Claw.OPEN, 3)
    servo.move(Wrist.UP, 3)
    servo.move(Arm.DOWN, 3)
