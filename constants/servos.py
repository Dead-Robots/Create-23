from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


# Yellow and Blue have tested values
class Arm(ServoEnum):
    port = ARM

    CUBE1 = ROBOT.choose(
        red=955,
        blue=1200,
        yellow=1160,
        green=760
    )

    CUBE1_DOWN = ROBOT.choose(
        red=1900,
        blue=2000,
        yellow=2000,
        green=150
    )

    CUBE2 = ROBOT.choose(
        red=10,
        blue=210,
        yellow=0,
        green=600
    )

    CUBE2_DOWN = ROBOT.choose(
        red=1450,
        blue=1660,
        yellow=1640,
        green=600
    )

    CUBE3 = ROBOT.choose(
        red=10,
        blue=210,
        yellow=0,
        green=600
    )

    CUBE3_DOWN = ROBOT.choose(
        red=950,
        blue=1210,
        yellow=1100,
        green=600
    )
    CUBE4_DOWN = ROBOT.choose(
        red=625,
        blue=850,
        yellow=690,
        green=600
    )

    UP = ROBOT.choose(
        red=525,
        blue=760,
        yellow=400,
        green=1000
    )

    DOWN = ROBOT.choose(
        red=1890,
        blue=2000,
        yellow=1970,
        green=150
    )

    HIGH = ROBOT.choose(
        red=550,
        blue=760,
        yellow=1400,
        green=1400
    )

    HIGHEST = ROBOT.choose(
        red=0,
        blue=160,
        yellow=0,
        green=1800
    )

    START = ROBOT.choose(
        red=1900,
        blue=2020,
        yellow=1800,
        green=0
    )


class Claw(ServoEnum):
    port = CLAW

    OPEN = ROBOT.choose(
        red=700,
        blue=675,
        yellow=360,
        green=200
    )

    CLOSED = ROBOT.choose(
        red=1700,
        blue=1900,
        yellow=1000,
        green=1000
    )


class Wrist(ServoEnum):
    port = WRIST

    START = ROBOT.choose(
        red=0,
        blue=0,
        yellow=1700,
        green=0
    )

    UP = ROBOT.choose(
        red=0,
        blue=0,
        yellow=0,
        green=0
    )

    HIGH = ROBOT.choose(
        red=1270,
        blue=1270,
        yellow=1270,
        green=1270
    )

    DOWN = ROBOT.choose(
        red=0,
        blue=0,
        yellow=500,
        green=500
    )

    SWEEP = ROBOT.choose(
        red=0,
        blue=100,
        yellow=600,
        green=600
    )

    CUBE1 = ROBOT.choose(
        red=680,
        blue=680,
        yellow=1060,
        green=160
    )

    CUBE1_DOWN = ROBOT.choose(
        red=0,
        blue=0,
        yellow=500,
        green=500
    )

    CUBE2 = ROBOT.choose(
        red=1550,
        blue=1650,
        yellow=2047,
        green=650
    )

    CUBE2_DOWN = ROBOT.choose(
        red=220,
        blue=220,
        yellow=630,
        green=600
    )

    CUBE3 = ROBOT.choose(
        red=1550,
        blue=1650,
        yellow=2047,
        green=650
    )

    CUBE3_DOWN = ROBOT.choose(
        red=680,
        blue=680,
        yellow=1080,
        green=600
    )

    CUBE4_DOWN = ROBOT.choose(
        # not set yet
        red=900,
        blue=900,
        yellow=1500,
        green=600
    )
