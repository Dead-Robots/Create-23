from kipr import msleep, disable_servos, enable_servos
import servo
from utilities import wait_for_button, start_button
from constants.servos import Claw, Wrist, Arm
from drive import drive, untimed_drive, square_up_tophats, square_up_white, gyro_turn
from common import ROBOT
from sensors import on_black_left, look_for_second_cube, look_for_third_cube, calibrate_gyro


# wait_for_button

def init():
    enable_servos()
    servo.move(Wrist.DOWN, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.DOWN, 1)
    # shutdown_create_in(119)


def shutdown():
    servo.move(Arm.START, 1)
    servo.move(Wrist.START, 1)
    servo.move(Claw.OPEN, 1)
    msleep(1000)
    disable_servos()


# start box position
def start_position():
    servo.move(Wrist.START, 1)
    servo.move(Arm.START, 1)
    servo.move(Claw.OPEN, 1)
    start_button()


def end_position():
    servo.move(Wrist.START, 1)
    servo.move(Arm.START, 1)
    servo.move(Claw.OPEN, 1)
    print('done with program')


def power_on_self_test():
    enable_servos()
    servo.move(Arm.UP, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Wrist.UP, 1)
    servo.move(Wrist.DOWN, 1)
    servo.move(Arm.DOWN, 1)
    servo.move(Claw.OPEN, 1)
    start_button()


def drive_straight_test():
    square_up_tophats(30, 30)


def wait(duration):
    msleep(100)
    drive(0, 0, duration)
    msleep(100)
    print('waiting')


def go_to_first_cube():
    print('first block')

    drive(40, 0, 230)
    servo.move(Claw.CLOSED, 0, 2)
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.CUBE1, 0)
    print('going forward')
    ROBOT.run(drive, red=(50, 50, 2000), yellow=(60, 60, 2000), blue=(60, 60, 2000))
    ROBOT.run(drive, yellow=(-40, 40, 900), blue=(-40, 38, 1000), red=(-40, 40, 1000))
    # first square up
    print('squaring up')
    ROBOT.run(drive, yellow=(40, 40, 1300), blue=(40, 40, 1700), red=(40, 40, 1700))
    ROBOT.run(drive, yellow=(-40, -40, 1250), blue=(-40, -40, 1350), red=(-40, -40, 1200))
    drive(40, -40, 850)
    # second square up
    drive(50, 50, 1550)
    # backing up
    ROBOT.run(drive, yellow=(-50, -45, 900), blue=(-50, -50, 875), red=(-50, -50, 875))
    # grab cube
    servo.move(Claw.OPEN, 1, 2)
    servo.move(Wrist.CUBE1, 1)
    servo.move(Arm.CUBE1, 1)
    servo.move(Claw.CLOSED, 1, 2)
    msleep(500)
    servo.move(Arm.HIGHEST, 1)
    servo.move(Wrist.HIGH, 1)


def go_to_analysis_lab1():
    print('analysis lab1')
    # backing up
    ROBOT.run(drive, yellow=(-25, -25, 450), blue=(-25, -25, 450), red=(-25, -25, 425))
    # rotate towards analysis lab
    ROBOT.run(drive, yellow=(40, -40, 800), blue=(40, -40, 850), red=(40, -40, 850))
    wait(2000)
    ROBOT.run(drive, yellow=(66, 60, 2000), blue=(60, 60, 2000), red=(60, 60, 2000))
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(-25, -25, 400)
    drive(40, -40, 875)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(0, 0, 175), blue=(-30, -30, 150), red=(-30, -30, 200))
    servo.move(Wrist.DOWN, 1, 2)
    servo.move(Arm.CUBE1_DOWN, 1)
    msleep(500)
    servo.move(Claw.OPEN, 1, 2)
    msleep(400)
    drive(-40, -40, 450)


def go_to_second_cube():
    print('second block')
    # arm and wrist up
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.CUBE2, 1, 2)
    # rotate 90 degrees right
    drive(40, -40, 950)
    # move forwards
    drive(40, 40, 1200)
    # rotate 90 degrees right
    drive(40, -40, 850)
    # square up
    drive(50, 50, 1600)
    msleep(100)
    # grab cube
    # backing up
    ROBOT.run(drive, yellow=(0, 0, 600), blue=(0, 0, 600), red=(-25, -25, 400))
    # place wrist and arm
    servo.move(Arm.CUBE2, 1, 2)
    # grab cube
    servo.move(Claw.CLOSED, 1, 2)
    msleep(450)
    servo.move(Arm.HIGHEST, 1, 2)
    msleep(300)
    servo.move(Wrist.HIGH, 1, 2)
    wait(2000)
    drive(-25, -25, 1300)


def go_to_analysis_lab2():
    print('analysis lab2')
    # rotate
    drive(40, -40, 900)
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(0, 0, 0)
    untimed_drive(-10, -10)
    while on_black_left():
        pass
    drive(-25, -25, 300)
    ROBOT.run(drive, yellow=(40, -40, 875), blue=(40, -40, 875), red=(38, -40, 865))
    second_cube_down()


def second_cube_down():
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(-25, -25, 650), blue=(-25, -25, 600), red=(-25, -25, 550))
    servo.move(Wrist.CUBE2_DOWN, 1, 2)
    servo.move(Arm.CUBE2_DOWN, 1)
    msleep(250)
    # deliver second log
    servo.move(Claw.OPEN, 1, 2)
    drive(-40, -40, 500)
    servo.move(Arm.HIGHEST, 1, 2)
    drive(25, 25, 500)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)


def go_to_third_cube():
    print('third block')
    # towards cube 3
    ROBOT.run(drive, yellow=(42, 40, 2200), blue=(40, 40, 2700), red=(40, 40, 2700))
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    drive(-40, 40, 850)
    msleep(100)
    drive(50, 50, 1200)
    msleep(100)
    # backing up
    ROBOT.run(drive, yellow=(-50, -50, 600), blue=(-50, -50, 600), red=(-50, -50, 700))    # place wrist and arm
    servo.move(Arm.CUBE2, 1)
    servo.move(Wrist.CUBE3, 1, 2)
    drive(40, 40, 800)
    # grab cube
    servo.move(Claw.CLOSED, 1, 2)
    msleep(450)
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.HIGH, 1)
    ROBOT.run(drive, yellow=(-25, -25, 1200), blue=(-25, -25, 650), red=(-25, -25, 650))


def go_to_analysis_lab3():
    print("analysis lab 3")
    drive(-25, -25, 900)
    ROBOT.run(drive, yellow=(-40, 40, 950), blue=(-35, 40, 950), red=(-35, 40, 950))
    square_up_tophats(40, 40)  # yellow is 42, 40
    square_up_white(-5, -5)
    drive(25, 25, 1850)
    drive(-40, 40, 900)
    third_cube_down()


def third_cube_down():
    square_up_tophats(15, 15)
    look_for_second_cube()
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(-25, -25, 835), blue=(-25, -25, 745), red=(-25, -25, 800))
    # delivery
    msleep(100)
    servo.move(Wrist.CUBE3_DOWN, 1)
    msleep(100)
    servo.move(Arm.CUBE3_DOWN, 1)
    msleep(400)
    servo.move(Claw.OPEN, 1)


def go_to_fourth_block():
    print('fourth block')
    drive(-25, -25, 600)
    servo.move(Arm.HIGHEST, 1, 2)
    drive(25, 25, 600)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(42, 40, 4200), blue=(60, 60, 3175), red=(60, 60, 3100))
    msleep(100)
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    drive(-40, 40, 850)
    msleep(100)
    drive(50, 50, 1550)

    # backing up
    ROBOT.run(drive, yellow=(-50, -45, 900), blue=(-50, -50, 850), red=(-50, -50, 850))
    # grab cube
    servo.move(Wrist.CUBE1, 1)
    servo.move(Arm.CUBE1, 1)
    servo.move(Claw.CLOSED, 1, 3)
    msleep(500)
    servo.move(Arm.HIGHEST, 1)
    servo.move(Wrist.HIGH, 1)
    ROBOT.run(drive, yellow=(-25, -25, 450), blue=(0, 0, 0), red=(0, 0, 0))


def go_to_analysis_lab4():
    print("analysis lab 4")
    ROBOT.run(drive, yellow=(-40, 40, 950), blue=(-40, 40, 930), red=(-40, 40, 930))
    ROBOT.run(drive, yellow=(40, 40, 3500), blue=(60, 60, 2200), red=(60, 60, 2200))  # yellow untested
    square_up_tophats(40, 40)  # yellow is 42, 40
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(25, 25, 1850), blue=(25, 25, 1850), red=(25, 25, 1850))
    drive(-40, 40, 900)
    fourth_cube_down()


def fourth_cube_down():
    square_up_tophats(15, 15)
    look_for_third_cube()
    square_up_white(-5, -5)
    drive(-25, -25, 825)
    msleep(100)
    servo.move(Wrist.CUBE4_DOWN, 1)
    msleep(100)
    servo.move(Arm.CUBE4_DOWN, 1)
    msleep(250)
    servo.move(Claw.OPEN, 1)
    drive(-25, -25, 500)


def test_turn_for_gyro():
    wait_for_button()
    msleep(500)
    calibrate_gyro()
    wait_for_button()
    gyro_turn(-30, 30, 360)

    # TODO: Change code for red robot, we didn't get to it today 4/3/23
