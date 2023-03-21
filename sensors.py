from constants.ports import *
from kipr import msleep, analog

def on_black_left():
    if analog(LEFT_TOPHAT) > 2000:
        return True
    else:
        return False

