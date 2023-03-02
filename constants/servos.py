from common import ROBOT
from common.core.enums import ServoEnum
from constants.ports import *


# Yellow has tested values
class Arm(ServoEnum):
    port = ARM

    DOWN = ROBOT.choose(
        red=150,
        blue=150,
        yellow=150,
        green=150
    )

    FIRST_CUBE = ROBOT.choose(
        red=680,
        blue=680,
        yellow=680,
        green=680
    )

    TWO = ROBOT.choose(
        red=820,
        blue=820,
        yellow=820,
        green=820
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


class Claw(ServoEnum):
    port = CLAW

    FIRST_CUBE_1 = ROBOT.choose(
        red=300,
        blue=300,
        yellow=300,
        green=300
    )

    OPEN = ROBOT.choose(
        red=600,
        blue=600,
        yellow=600,
        green=600
    )

    CLOSED_CUBE_1 = ROBOT.choose(
        red=900,
        blue=900,
        yellow=900,
        green=900
    )

    CLOSED = ROBOT.choose(
        red=950,
        blue=950,
        yellow=950,
        green=950
    )


class Wrist(ServoEnum):
    port = WRIST

    UP = ROBOT.choose(
        red=0,
        blue=0,
        yellow=0,
        green=0
    )

    FIRST = ROBOT.choose(
        red=160,
        blue=160,
        yellow=160,
        green=160
    )

    DOWN = ROBOT.choose(
        red=500,
        blue=500,
        yellow=500,
        green=500
    )

    TWO = ROBOT.choose(
        red=700,
        blue=700,
        yellow=700,
        green=700
    )

    HIGH = ROBOT.choose(
        red=1270,
        blue=1270,
        yellow=1270,
        green=1270
    )
