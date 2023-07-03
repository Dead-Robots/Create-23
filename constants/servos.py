from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


def translate_arm(angle):
    position = int(angle / 175 * 2047 + ROBOT.choose(red=150, green=122))
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
    return position


def translate_claw(angle):
    position = int(angle / 175 * 2047 + ROBOT.choose(red=1700, green=1666))
    if position < 0 or position > 2047:
        raise Exception("Resulting position invalid " + str(position) + " " + str(angle))
    return position


# Yellow and Blue have tested values
class Arm(ServoEnum):  # please keep in order :)
    port = ARM
    translation_function = translate_arm

    # Driving positions
    START = 2047
    STRAIGHT_UP = translate_arm(15)
    UP = translate_arm(25)
    DRIVING_RELAXED = translate_arm(143)
    REST_POSITION = translate_arm(153)

    # POST Value
    NINETY = translate_arm(90)

    # Pickup Values
    RED_RING_PICKUP = translate_arm(ROBOT.choose(red=104, green=116))
    ORANGE_RING_PICKUP = translate_arm(ROBOT.choose(red=111, green=121))
    YELLOW_RING_PICKUP = translate_arm(ROBOT.choose(red=118, green=130))
    GREEN_RING_PICKUP = translate_arm(ROBOT.choose(red=126, green=139))
    BLUE_RING_PICKUP = translate_arm(ROBOT.choose(red=135, green=146.5))

    # Delivery Values
    SHORT_RING_UP = translate_arm(ROBOT.choose(red=42, green=54))
    SHORT_RING_DOWN = translate_arm(ROBOT.choose(red=73, green=85))
    DELIVER_SHORT_RING = translate_arm(ROBOT.choose(red=66, green=78))
    TALL_RING_DELIVERY = translate_arm(ROBOT.choose(red=9, green=15))
    YELLOW_RING_DELIVERY = translate_arm(ROBOT.choose(red=20, green=26))


class Claw(ServoEnum):
    port = CLAW
    translation_function = translate_claw

    OPEN = translate_claw(-40)
    CLOSED = translate_claw(14)
    RED_RING = translate_claw(20)
    YELLOW_RING = translate_claw(27)
