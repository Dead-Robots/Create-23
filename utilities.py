# from common.drive import stop_motors
from kipr import msleep, push_button

import servo
from constants.servos import Claw, Wrist, Arm


def wait_for_button():
    # stop_motors()
    print("Waiting for button")
    while not push_button():
        pass
    msleep(1000)


def arm_resting():
    wait_for_button()
    servo.move(Claw.OPEN, 1)
    servo.move(Wrist.DOWN, 1)
    servo.move(Arm.DOWN, 3)