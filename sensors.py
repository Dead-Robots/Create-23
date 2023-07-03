from constants.ports import *
from kipr import analog, gyro_z, msleep


def on_black_left(threshold=1500):
    if analog(LEFT_TOPHAT) > threshold:
        return True
    else:
        return False


def on_black_right(threshold=1500):
    if analog(RIGHT_TOPHAT) > threshold:
        return True
    else:
        return False


gyro_offset = 0


def gyroscope():
    return gyro_z() - gyro_offset


def calibrate_gyro():
    total = 0
    for x in range(50):
        total = total + gyro_z()
        msleep(10)
    global gyro_offset
    gyro_offset = total / 50


# def look_for_second_cube():
#     print('looking for second cube')
#     et_value = analog(LOWER_ET)
#     if et_value > 1550:
#         print('block here')
#         return True
#     else:
#         print('2nd block missing')
#         return False
#
#
# def look_for_third_cube():
#     print('looking for third cube')
#     et_value = analog(UPPER_ET)
#     if et_value > 1550:
#         print('2nd block here')
#         return True
#     else:
#         print('3rd block missing')
#         return False
#
#
# def test_et(et_port):
#     print("testing et in port", et_port)
#     if analog(et_port) > 1550:
#         print("et in port", et_port, "already sees object")
#     while analog(et_port) > 1550:
#         pass
#     while analog(et_port) < 1550:
#         pass
#     while analog(et_port) > 1550:
#         pass
#     print("et in port", et_port, "is ok")
