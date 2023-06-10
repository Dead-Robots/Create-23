#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from actions import init, shutdown, power_on_self_test, start_position, end_position, get_first_ring, move_rings, \
    push_rings, testing
from common import ROBOT
from utilities import wait_for_button


def main():
    init()
    push_rings()
    # get_first_ring()
    # move_rings()

    shutdown()


if __name__ == '__main__':
    print("I am", ROBOT.value)
    with CreateConnection():
        main()
    shutdown()
