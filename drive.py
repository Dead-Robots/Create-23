from kipr import msleep, disable_servos, enable_servos
from createserial.commands import create_dd
import servo
from utilities import wait_for_button
from constants.servos import Claw, Wrist, Arm


def drive(left_speed, right_speed, duration):
    create_dd(-5 * right_speed, -5 * left_speed)
    msleep(duration)
    create_dd(0, 0)


def untimed_drive(left_speed, right_speed):
    create_dd(-5 * right_speed, -5 * left_speed)





