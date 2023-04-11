from constants.ports import *
from kipr import analog


def on_black_left():
    if analog(LEFT_TOPHAT) > 1500:
        return True
    else:
        return False


def on_black_right():
    if analog(RIGHT_TOPHAT) > 1500:
        return True
    else:
        return False


def look_for_second_cube():
    print('looking for second cube')
    et_value = analog(LOWER_ET)
    if et_value > 1550:
        print('block here')
    else:
        print('block missing')


def look_for_third_cube():
    print('looking for third cube')
    et_value = analog(UPPER_ET)
    if et_value > 1550:
        print('block here')
    else:
        print('block missing')
