from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


def translate_arm(angle):
    position = int(angle / 175 * 2047 + 0)
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position))
    return position


def translate_claw(angle):
    position = int(angle / 175 * 2047 + 200)
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position))
    return position


def translate_wrist(angle):
    position = int(angle / 175 * 2047 + 156)
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position))
    return position


# Yellow and Blue have tested values
class Arm(ServoEnum):
    port = ARM
    translation_function = translate_arm
    HUNDRED = translate_arm(100)
    ZERO = translate_arm(0)
    NINETY = translate_arm(90)
    FORTY = translate_arm(40)
    HUNDRED_TEN = translate_arm(110)
    HUNDRED_TWENTY = translate_arm(120)
    HUNDRED_TWENTY_FIVE = translate_arm(125)
    HUNDRED_THIRTY = translate_arm(130)
    HUNDRED_FIFTEEN = translate_arm(115)
    # HUNDRED_THIRTY_FIVE = translate_arm(135)
    # HUNDRED_FORTY = translate_arm(140)


class Claw(ServoEnum):
    port = CLAW
    translation_function = translate_claw
    HUNDRED = translate_claw(100)
    TWENTY = translate_claw(20)
    HUNDRED_TEN = translate_claw(110)
    HUNDRED_FIVE = translate_claw(105)
    ZERO = translate_claw(0)
    NINETY = translate_claw(90)
    FORTY = translate_claw(40)


class Wrist(ServoEnum):
    port = WRIST
    ZERO = translate_wrist(0)


