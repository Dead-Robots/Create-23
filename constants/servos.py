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
    END_POSITION = 1550
    HUNDRED = translate_arm(100)
    ZERO = translate_arm(0)
    NINETY = translate_arm(90)
    FORTY = translate_arm(40)
    HUNDRED_TEN = translate_arm(110)
    HUNDRED_TWENTY = translate_arm(120)
    HUNDRED_TWENTY_FIVE = translate_arm(125)
    HUNDRED_THIRTY = translate_arm(130)
    HUNDRED_FIFTEEN = translate_arm(115)
    ONE_THIRTY_EIGHT = translate_arm(138)
    ONE_THIRTY_SIX = translate_arm(136)
    ONE_SEVENTY = translate_arm(170)
    PUSH_RINGS = 1750
    # HUNDRED_THIRTY_FIVE = translate_arm(135)
    # HUNDRED_FORTY = translate_arm(140)
    RING_DROP = 1640
    RING_UP = 700
    RED_RING = 1150
    ORANGE_RING = 1250
    YELLOW_RING = 1350


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
    OPEN = 2047
    CLOSED = translate_claw(105)
    RED_RING = 1400
    ORANGE_RING = 1425
    YELLOW_RING = 1450
    CLOSED_RING_STAND = translate_claw(100)


class Wrist(ServoEnum):
    port = WRIST
    translation_function = translate_wrist
    ZERO = translate_wrist(0)
    NEGATIVE_SIX = translate_wrist(-6)
    RING_DROP = 1700
    RED_RING = 1875
    ORANGE_RING = 1750
    YELLOW_RING = 1700
    PUSH_RINGS = 1330

