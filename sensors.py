from constants.ports import *
from kipr import msleep, analog

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
