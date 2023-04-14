from kipr import msleep
from createserial.commands import create_dd
from sensors import on_black_left, on_black_right, gyroscope


def drive(left_speed, right_speed, duration):
    create_dd(-5 * right_speed, -5 * left_speed)
    msleep(duration)
    create_dd(0, 0)


def untimed_drive(left_speed, right_speed):
    create_dd(-5 * right_speed, -5 * left_speed)


def square_up_tophats(left_speed, right_speed):
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
    untimed_drive(left_speed, right_speed)
    current_turned_distance = 0
    while abs(current_turned_distance) < abs(angle):
        current_turned_distance += gyroscope() * 25/1000 / 8
        msleep(25)
    untimed_drive(0, 0)
