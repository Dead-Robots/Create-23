from kipr import push_button, msleep, disable_servos, enable_servos, enable_servo, get_servo_position, \
    set_servo_position
from createserial.commands import open_create, reset_create, create_dd
from createserial.serial import open_serial
from common import servo
from constants.ports import ARM, WRIST, CLAW
from constants.servos import Claw, Wrist, Arm

from main import arm_down, wrist_up, claw_open, arm_up, claw_closed, wrist_down, first_wrist, claw_first_cube1, \
    wrist_2, arm_2, claw_closed_cube1, arm_high, wrist_high


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create
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


def got_to_first_block():
    print('first block')
    move(arm_up, 1, ARM)
    move(first_wrist, 1, WRIST)
    move(claw_first_cube1, 1, CLAW)

    # turning
    drive(40, 0, 230)
    msleep(100)
    drive(50, 50, 3500)
    msleep(2000)
    #grab cube

    #backing up
    drive(-50, -45, 1000)
    move(wrist_2, 1, WRIST)
    msleep(1000)
    move(arm_2, 1, ARM)
    msleep(1000)
    move(claw_closed_cube1, 1, CLAW)
    #move(arm_first_cube, 1, arm)
    msleep(2000)
    move(arm_up, 1, ARM)
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
    move(wrist_up, 1, WRIST)
    msleep(100)
    move(arm_down, 1, ARM)
    msleep(100)
    move(300, 1, CLAW)
    msleep(1000)


def got_to_second_block():
    print('second block')
    drive(-25, -25, 750)
    move(1800, 1, ARM)
    msleep(500)
    drive(0, 40, 700)
    drive(40, 40, 2250)
    move(arm_high, 1, ARM)
    move(wrist_high, 1, WRIST)
    drive(-40, 40, 925)
    msleep(500)
    drive(40, 40, 750)
    msleep(100)
    move(claw_closed_cube1, 1, CLAW)
    msleep(100)
    move(wrist_up, 1, WRIST)
    msleep(100)
    drive(-40, 40, 1800)
    move(600, 1, WRIST)
    move(600, 1, ARM)
    move(claw_open, 1, CLAW)
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


def drive(lm, rm, time):
    create_dd(-5 * rm, -5 * lm)
    msleep(time)
    create_dd(0, 0)


def arm_resting():
    #wait_for_button()
    move(claw_open, 3, CLAW)
    move(wrist_up, 3, WRIST)
    move(arm_down, 3, ARM)
