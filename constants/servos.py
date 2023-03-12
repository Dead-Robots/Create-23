from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


# Yellow has tested values
class Arm(ServoEnum):
    port = ARM

    DOWN = ROBOT.choose(
        red=1890,
        blue=150,
        yellow=150,
        green=150
    )

    CUBE2 = ROBOT.choose(
        red=430,
        blue=600,
        yellow=600,
        green=600
    )

    CUBE1 = ROBOT.choose(
        red=1060,
        blue=760,
        yellow=760,
        green=760
    )

    UP = ROBOT.choose(
        red=1000,
        blue=1000,
        yellow=1000,
        green=1000
    )

    HIGH = ROBOT.choose(
        red=1400,
        blue=1400,
        yellow=1400,
        green=1400
    )

    HIGHEST = ROBOT.choose(
        red=0,
        blue=1800,
        yellow=1800,
        green=1800
    )


class Claw(ServoEnum):
    port = CLAW

    OPEN = ROBOT.choose(
        red=450,
        blue=200,
        yellow=200,
        green=200
    )

    CLOSED = ROBOT.choose(
        red=1000,
        blue=1000,
        yellow=1000,
        green=1000
    )


class Wrist(ServoEnum):
    port = WRIST

    UP = ROBOT.choose(
        red=0,
        blue=0,
        yellow=0,
        green=0
    )

    CUBE1 = ROBOT.choose(
        red=1330,
        blue=160,
        yellow=160,
        green=160
    )

    DOWN = ROBOT.choose(
        red=790,
        blue=500,
        yellow=500,
        green=500
    )

    CUBE2 = ROBOT.choose(
        red=2040,
        blue=650,
        yellow=650,
        green=650
    )

    HIGH = ROBOT.choose(
        red=1270,
        blue=1270,
        yellow=1270,
        green=1270
    )