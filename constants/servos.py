from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


# Yellow and Blue have tested values
class Arm(ServoEnum):
    port = ARM

    CUBE1 = ROBOT.choose(
        red=965,
        blue=1000,
        yellow=1160,
        green=760
    )

    CUBE1_DOWN = ROBOT.choose(
        red=1850,
        blue=1760,
        yellow=2000,
        green=150
    )

    CUBE2 = ROBOT.choose(
        red=120,
        blue=80,
        yellow=0,
        green=600
    )

    CUBE2_DOWN = ROBOT.choose(
        red=1380,
        blue=1500,
        yellow=1640,
        green=600
    )

    CUBE3_DOWN = ROBOT.choose(
        red=935,
        blue=1010,
        yellow=1100,
        green=600
    )
    CUBE4_DOWN = ROBOT.choose(
        red=600,
        blue=690,
        yellow=690,
        green=600
    )

    UP = ROBOT.choose(
        red=630,
        blue=600,
        yellow=400,
        green=1000
    )

    DOWN = ROBOT.choose(
        red=1890,
        blue=2040,
        yellow=1970,
        green=150
    )

    HIGH = ROBOT.choose(
        red=1400,
        blue=600,
        yellow=1400,
        green=1400
    )

    HIGHEST = ROBOT.choose(
        red=0,
        blue=0,
        yellow=0,
        green=1800
    )

    START = ROBOT.choose(
        red=1900,
        blue=1860,
        yellow=1800,
        green=0
    )


class Claw(ServoEnum):
    port = CLAW

    OPEN = ROBOT.choose(
        red=745,
        blue=675,
        yellow=360,
        green=200
    )

    CLOSED = ROBOT.choose(
        red=2000,
        blue=1900,
        yellow=1000,
        green=1000
    )


class Wrist(ServoEnum):
    port = WRIST

    START = ROBOT.choose(
        red=180,
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
        red=1340,
        blue=1270,
        yellow=1270,
        green=1270
    )

    DOWN = ROBOT.choose(
        red=340,
        blue=0,
        yellow=500,
        green=500
    )

    CUBE1 = ROBOT.choose(
        red=1100,
        blue=680,
        yellow=1060,
        green=160
    )

    CUBE2 = ROBOT.choose(
        red=1925,
        blue=1710,
        yellow=2047,
        green=650
    )

    CUBE2_DOWN = ROBOT.choose(
        red=1040,
        blue=220,
        yellow=630,
        green=600
    )

    CUBE3 = ROBOT.choose(
        red=2010,
        blue=1650,
        yellow=2047,
        green=650
    )

    CUBE3_DOWN = ROBOT.choose(
        red=1566,
        blue=680,
        yellow=1080,
        green=600
    )

    CUBE4_DOWN = ROBOT.choose(
        # not set yet
        red=1370,
        blue=900,
        yellow=1500,
        green=600
    )
