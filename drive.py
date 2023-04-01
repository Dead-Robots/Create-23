from kipr import msleep, disable_servos, enable_servos
from createserial.commands import create_dd
import servo
from utilities import wait_for_button
from constants.servos import Claw, Wrist, Arm
from sensors import on_black_left, on_black_right


def drive(left_speed, right_speed, duration):
    create_dd(-5 * right_speed, -5 * left_speed)
    msleep(duration)
    create_dd(0, 0)


def untimed_drive(left_speed, right_speed):
    create_dd(-5 * right_speed, -5 * left_speed)


def square_up_tophats(left_speed, right_speed):
    untimed_drive(left_speed, right_speed)
    while left_speed!=0 or right_speed!=0:
        if on_black_left():
            left_speed = 0
            untimed_drive(left_speed, right_speed)
        if on_black_right():
            right_speed = 0
            untimed_drive(left_speed, right_speed)
    untimed_drive(0, 0)


def square_up_white(left_speed, right_speed):
    untimed_drive(left_speed, right_speed)
    while left_speed!=0 or right_speed!=0:
        if not on_black_left():
            left_speed = 0
            untimed_drive(left_speed, right_speed)
        if not on_black_right():
            right_speed = 0
            untimed_drive(left_speed, right_speed)
    untimed_drive(0, 0)
