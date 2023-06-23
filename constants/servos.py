from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


def translate_arm(angle):
    position = int(angle / 175 * 2047 + ROBOT.choose(red=175, green=-139))
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
    return position


def translate_claw(angle):
    position = int(angle / 175 * 2047 + ROBOT.choose(red=1450, green=1560))
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
    return position


# Yellow and Blue have tested values
class Arm(ServoEnum):
    port = ARM
    translation_function = translate_arm
    REST_POSITION = translate_arm(143)
    HUNDRED = translate_arm(100)
    STRAIGHT_UP = translate_arm(15)
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
