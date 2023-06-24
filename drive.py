import time
from math import copysign

from kipr import msleep
from createserial.commands import create_dd

from common.gyro_movements import straight_drive
from sensors import on_black_left, on_black_right, gyroscope


def drive(left_speed, right_speed, duration):
    create_dd(-5 * right_speed, -5 * left_speed)
    msleep(duration)
    create_dd(0, 0)


def stop_motors():
    create_dd(0, 0)


def untimed_drive(left_speed, right_speed):
    create_dd(-5 * right_speed, -5 * left_speed)


def square_up_black(left_speed, right_speed):
    untimed_drive(left_speed, right_speed)
    while left_speed != 0 or right_speed != 0:
        if on_black_left():
            left_speed = 0
            untimed_drive(left_speed, right_speed)
        if on_black_right():
            right_speed = 0
            untimed_drive(left_speed, right_speed)
    untimed_drive(0, 0)


def square_up_white(left_speed, right_speed):
    untimed_drive(left_speed, right_speed)
    while left_speed != 0 or right_speed != 0:
        if not on_black_left():
            left_speed = 0
            untimed_drive(left_speed, right_speed)
        if not on_black_right():
            right_speed = 0
            untimed_drive(left_speed, right_speed)
    untimed_drive(0, 0)


def gyro_turn(left_speed, right_speed, angle):
    old_time = time.time()
    untimed_drive(left_speed, right_speed)
    current_turned_distance = 0
    while abs(current_turned_distance) < abs(angle):
        current_turned_distance += gyroscope() * (time.time() - old_time) / 8
        old_time = time.time()
        msleep(10)
    untimed_drive(0, 0)


def gyro_turn_with_slow_down(left_speed, right_speed, angle):
    fast_angle = 0.50 * angle
    slow_angle = angle - fast_angle
    gyro_turn(left_speed, right_speed, fast_angle)
    gyro_turn(int(copysign(10, left_speed)), int(copysign(10, right_speed)), slow_angle)


def straight_drive_black(speed):
    def see_white():
        return not on_black_left() and not on_black_right()
    straight_drive(speed, see_white)
