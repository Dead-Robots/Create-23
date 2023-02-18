#!/usr/local/bin/python3.10 -u
from createserial.commands import reset_create, close_create, open_create, create_dd
from createserial.serial import open_serial, close_serial
from kipr import motor_power, msleep, enable_servos, set_servo_position

LEFT_MOTOR=3
RIGHT_MOTOR=0


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create


def end():
    # Terminate communications with the Create
    close_create()

    # Close serial port connection to the Create
    close_serial()


def fixed_dd(lm, rm):
    create_dd(-rm, -lm)


def grab_lower_block():
    # go to block
    fixed_dd(335, 300)
    msleep(2840)
    fixed_dd(0, 0)
    msleep(2000)

    # go back
    fixed_dd(-300, -300)
    msleep(2000)
    fixed_dd(0, 0)
    msleep(250)

    # right turn
    fixed_dd(320, -300)
    msleep(600)
    fixed_dd(0, 0)
    msleep(2000)

    # leave analysis lab
    fixed_dd(-300, -300)
    msleep(100)
    fixed_dd(0, 0)
    msleep(250)
    fixed_dd(-300, 0)
    msleep(615)
    fixed_dd(0, 0)
    msleep(250)

    # go to 2nd block
    fixed_dd(300, 300)
    msleep(2500)
    fixed_dd(0, 0)
    msleep(250)

    # turn to 2nd block
    fixed_dd(0, 200)
    msleep(750)
    fixed_dd(0, 0)
    msleep(250)
    fixed_dd(300, 300)
    msleep(500)
    fixed_dd(0, 0)
    msleep(2000)

    # # back to analysis lab
    # fixed_dd(-300, -300)
    # msleep(1000)
    # fixed_dd(0, 0)
    # msleep(1000)
    # fixed_dd(-320, -100)
    # msleep(1500)
    # fixed_dd(0, 0)
    # msleep(1500)

    # # right turn
    # fixed_dd(-300, 320)
    # msleep(600)
    # fixed_dd(0, 0)
    # msleep(2000)










# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    grab_lower_block()
    end()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
