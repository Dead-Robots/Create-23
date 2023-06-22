from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


def translate_arm(angle):
    position = int(angle / 175 * 2047 + 175)
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
    return position


def translate_claw(angle):
    position = int(angle / 175 * 2047 + 1450)  # was 200
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
    return position


def translate_wrist(angle):
    position = int(angle / 175 * 2047 + 156)
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
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
    # ONE_SEVENTY = translate_arm(170)
    PUSH_RINGS = 1600
    # HUNDRED_THIRTY_FIVE = translate_arm(135)
    # HUNDRED_FORTY = translate_arm(140)
    RING_DROP = 1640
    RING_UP = 700

    RED_RING = translate_arm(113)
    ORANGE_RING = translate_arm(120)
    YELLOW_RING = translate_arm(126)

    SIXTY = translate_arm(60)
    SEVENTY = translate_arm(70)
    SIXTY_FIVE = translate_arm(65)
    DELIVER_RED_RING = translate_arm(77)
    RED_RING_2 = translate_arm(60)
    RED_RING_DOWN = translate_arm(81)
    YELLOW_RING_DOWN = translate_arm(143)
    GREEN_RING = translate_arm(134)
    BLUE_RING = translate_arm(140)


class Claw(ServoEnum):
    port = CLAW
    translation_function = translate_claw
    OPEN = translate_claw(-23)
    CLOSED = translate_claw(8)
    RED_RING = translate_claw(25)
    # ORANGE_RING = 1425
    YELLOW_RING = translate_claw(27)
    # CLOSED_RING_STAND = translate_claw(100)


class Wrist(ServoEnum):
    port = WRIST
    translation_function = translate_wrist
    ZERO = translate_wrist(0)
    NEGATIVE_SIX = translate_wrist(-6)
    RING_DROP = 1325
    RED_RING = 1300  # was 1875
    ORANGE_RING = 1375
    YELLOW_RING = 1130
    PUSH_RINGS = 855
    PUSH_CUBE = 1650
