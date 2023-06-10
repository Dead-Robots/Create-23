from typing import Optional

from createserial.encoders import Encoders
from createserial.constants import Opcode
from createserial.serial import query_create
from kipr import msleep, disable_servos, enable_servos
import servo
from common.gyro_movements import gyro_init, gyro_turn, straight_drive_distance
from utilities import wait_for_button
from constants.servos import Claw, Wrist, Arm, translate_arm, translate_claw
from constants import ports
from drive import drive, untimed_drive, square_up_tophats, square_up_white, stop_motors
from common import ROBOT, light
from sensors import on_black_left, look_for_second_cube, look_for_third_cube, test_et
from createserial.shutdown import shutdown_create_in

encoders: Optional[Encoders] = None


def init():
    # print('Press button to calibrate gyro, do not move robot.')
    # wait_for_button("press button to cal gyros, DO NOT MOVE ROBOT!")
    # msleep(1000)
    enable_servos()
    gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.983, 0.094, 0.1, 0.3, 0.0)
    global encoders
    encoders = Encoders()
    wait_for_button()
    # print('Calibration Complete')


def move_rings():
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.RING_UP, 1)
    servo.move(Wrist.ZERO, 1)
    wait_for_button("Push button to start.")

    # red ring
    servo.move(Wrist.RED_RING, 1)
    servo.move(Arm.RED_RING, 1)
    msleep(500)
    servo.move(Claw.RED_RING, 1)
    msleep(500)
    servo.move(Arm.RING_UP, 1)
    # turn and place it down
    gyro_turn(-30, 30, 90, True)
    servo.move(Wrist.RING_DROP, 1)
    servo.move(Arm.RING_DROP, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.RING_UP, 1)
    gyro_turn(30, -30, 90, True)

    # orange ring
    servo.move(Wrist.ORANGE_RING, 1)
    servo.move(Arm.ORANGE_RING, 1)
    drive(-30, -30, 50)
    stop_motors()
    msleep(500)
    servo.move(Claw.ORANGE_RING, 1)
    msleep(500)
    servo.move(Arm.RING_UP, 1)
    # turn and place it down
    gyro_turn(-30, 30, 90, True)
    servo.move(Wrist.RING_DROP, 1)
    servo.move(Arm.RING_DROP, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.RING_UP, 1)
    gyro_turn(30, -30, 90, True)

    # yellow ring
    servo.move(Wrist.YELLOW_RING, 1)
    servo.move(Arm.YELLOW_RING, 1)
    drive(-30, -30, 100)
    stop_motors()
    msleep(500)
    servo.move(Claw.YELLOW_RING, 1)
    msleep(500)
    servo.move(Arm.RING_UP, 1)
    # turn and place it down
    gyro_turn(-30, 30, 90, True)
    servo.move(Wrist.RING_DROP, 1)
    servo.move(Arm.RING_DROP, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.RING_UP, 1)
    gyro_turn(30, -30, 90, True)
    drive(30, 30, 100)
    stop_motors()


def get_bumps():
    data = query_create([Opcode.QUERY_LIST, 1, 7], 1)
    return data != b'\x00'


def get_encoder_values():
    left, right = Encoders.values
    return -1 * left, -1 * right


def shutdown():
    # servo.move(Arm.START, 1)
    # servo.move(Wrist.START, 1)
    # servo.move(Claw.OPEN, 1)
    msleep(1000)
    servo.move(Arm.END_POSITION, 1)
    disable_servos()


# start box position
def start_position():
    enable_servos()
    servo.move(Claw.OPEN, 1)
    servo.move(Wrist.START, 1)
    servo.move(Arm.START, 1)
    light.wait_4_light(2)
    shutdown_create_in(119)


def end_position():
    servo.move(Wrist.START, 1)
    servo.move(Arm.START, 1)
    servo.move(Claw.OPEN, 1)
    print('done with program')


def power_on_self_test():
    wait_for_button("Push button to run self test.")
    enable_servos()
    square_up_tophats(10, 10)
    msleep(200)
    square_up_white(-10, -10)
    servo.move(Arm.UP, 1)
    # test ETs
    test_et(ports.LOWER_ET)
    test_et(ports.UPPER_ET)
    # test claw
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Wrist.HIGH, 1, 2)
    servo.move(Wrist.DOWN, 1, 2)
    servo.move(Wrist.HIGH, 1, 2)
    servo.move(Wrist.DOWN, 1, 2)
    servo.move(Wrist.START, 1, 2)
    servo.move(Arm.DOWN, 1)
    print("self test complete!")
    wait_for_button("Aim robot and push button to calibrate light sensor.")


def drive_straight_test():
    square_up_tophats(30, 30)


def wait(duration):
    msleep(100)
    drive(0, 0, duration)
    msleep(100)
    print('waiting')


def get_first_ring():
    enable_servos()
    servo.move(Arm.ZERO, 2)
    # make sure the claw is open before trying to grab the ring
    servo.move(Claw.TWENTY, 5, 2)
    wait_for_button("ready to start")
    # try getting the arm in the right position to pick up the ring
    servo.move(Arm.HUNDRED_FIFTEEN, 3)
    # need the wrist to be perpendicular to the board
    servo.move(Wrist.ZERO)
    # need to close claw in order to grab the ring
    servo.move(Claw.HUNDRED_TEN, 3)
    wait_for_button("is the arm in the position?")
    servo.move(Arm.FORTY, 0)
    wait_for_button("has the robot lifted ring?")
    # exit(0)


def go_to_first_cube():
    print('first block')
    drive(40, 0, 230)
    servo.move(Claw.CLOSED, 0, 2)
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.CUBE1, 0)
    print('going forward')
    ROBOT.run(drive, red=(50, 50, 2000), yellow=(60, 60, 2000), blue=(60, 60, 2000), green=(60, 60, 2000))
    gyro_turn(-40, 40, 92)
    # first square up
    print('squaring up')
    ROBOT.run(drive, yellow=(40, 40, 1300), blue=(40, 40, 1700), red=(40, 40, 1700), green=(40, 40, 1700))
    ROBOT.run(drive, yellow=(-40, -40, 1250), blue=(-40, -40, 1350), red=(-40, -40, 1200), green=(-40, -40, 1200))
    gyro_turn(40, -40, 81)
    # second square up
    drive(50, 50, 1550)
    # backing up
    ROBOT.run(drive, yellow=(-50, -45, 900), blue=(-50, -50, 875), red=(-50, -50, 835), green=(-50, -50, 875))
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
    ROBOT.run(drive, yellow=(-25, -25, 450), blue=(-25, -25, 450), red=(-25, -25, 425), green=(-25, -25, 450))
    # rotate towards analysis lab
    gyro_turn(40, -40, 81)
    ROBOT.run(drive, yellow=(66, 60, 2000), blue=(60, 60, 2000), red=(62, 60, 2000), green=(60, 60, 2000))
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(-25, -25, 400)
    place_first_cube()


def place_first_cube():
    servo.move(Wrist.SWEEP, 1, 2)
    servo.move(Wrist.CUBE1_DOWN, 1, 2)
    servo.move(Arm.CUBE1_DOWN, 1)
    gyro_turn(40, -40, 81)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(0, 0, 175), blue=(30, 30, 50), red=(-30, -30, 0), green=(30, 30, 50))
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
    gyro_turn(40, -40, 81)
    # move forwards
    ROBOT.run(drive, yellow=(40, 40, 1050), blue=(40, 40, 1150), red=(50, 50, 1050), green=(40, 40, 1150))
    # rotate 90 degrees right
    drive(40, -40, 850)
    # square up
    ROBOT.run(drive, yellow=(50, 50, 1600), blue=(50, 50, 1600), red=(50, 50, 1250), green=(50, 50, 1600))
    msleep(100)
    # backing up
    ROBOT.run(drive, yellow=(0, 0, 600), blue=(-25, -25, 150), red=(-25, -25, 150), green=(-25, -25, 150))
    # place wrist and arm
    servo.move(Arm.CUBE2, 1, 2)  # red messes up
    # grab cube
    servo.move(Claw.CLOSED, 1, 2)
    msleep(450)
    servo.move(Arm.HIGHEST, 1, 2)
    msleep(300)
    servo.move(Wrist.UP, 1, 2)
    drive(-25, -25, 300)
    wait(1700)
    drive(-25, -25, 950)


def go_to_analysis_lab2():
    print('analysis lab2')
    # rotate
    gyro_turn(40, -40, 81)
    square_up_tophats(42, 40)
    square_up_white(-5, -5)
    drive(0, 0, 0)
    untimed_drive(-10, -10)
    while on_black_left():
        pass
    drive(-25, -25, 300)
    ROBOT.run(drive, yellow=(40, -40, 875), blue=(40, -40, 875), red=(38, -40, 865), green=(40, -40, 875))
    second_cube_down()


def second_cube_down():
    place_second_cube()
    ROBOT.run(drive, yellow=(-40, -40, 0), blue=(-40, -40, 500), red=(-40, -40, 500), green=(-40, -40, 500))
    servo.move(Arm.HIGHEST, 1, 2)
    drive(25, 25, 500)
    drive(-40, 40, 900)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)


def place_second_cube():
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(-25, -25, 650), blue=(-25, -25, 600), red=(-25, -25, 675), green=(-25, -25, 600))
    servo.move(Wrist.CUBE2_DOWN, 1, 2)
    servo.move(Arm.CUBE2_DOWN, 1)
    msleep(250)
    # deliver second log
    servo.move(Claw.OPEN, 1, 2)


def go_to_third_cube():
    print('third block')
    # towards cube 3
    ROBOT.run(drive, yellow=(42, 40, 2200), blue=(40, 40, 2750), red=(41, 40, 2700), green=(40, 40, 2750))
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    gyro_turn(-40, 40, 81)
    msleep(100)
    drive(50, 50, 1200)
    msleep(100)
    # backing up
    ROBOT.run(drive, yellow=(-50, -50, 600), blue=(-50, -50, 600), red=(-50, -50, 700), green=(-50, -50, 600))
    # place wrist and arm
    servo.move(Arm.CUBE2, 1)
    servo.move(Wrist.CUBE3, 1, 2)
    drive(40, 40, 800)
    # grab cube
    servo.move(Claw.CLOSED, 1, 2)
    msleep(450)
    servo.move(Arm.HIGHEST, 1, 2)
    servo.move(Wrist.HIGH, 1)
    ROBOT.run(drive, yellow=(-25, -25, 1200), blue=(-25, -25, 650), red=(-25, -25, 650), green=(-25, -25, 650))


def go_to_analysis_lab3():
    print("analysis lab 3")
    drive(-25, -25, 900)
    ROBOT.run(drive, yellow=(-40, 40, 950), blue=(-35, 40, 950), red=(-35, 40, 950), green=(-35, 40, 950))
    square_up_tophats(40, 40)  # yellow is 42, 40
    square_up_white(-5, -5)
    drive(25, 25, 1850)
    drive(-40, 40, 900)
    cube_down()


def third_cube_down():
    place_third_cube()


def place_third_cube():
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(-25, -25, 835), blue=(-25, -25, 645), red=(-25, -25, 800), green=(-25, -25, 645))
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
    gyro_turn(-40, 40, 81)
    square_up_tophats(15, 15)
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(42, 40, 4200), blue=(60, 60, 3175), red=(64, 60, 3100), green=(60, 60, 3175))
    msleep(100)
    servo.move(Arm.HIGHEST, 1)
    msleep(100)
    gyro_turn(-40, 40, 81)
    msleep(100)
    drive(50, 50, 1550)
    # backing up
    ROBOT.run(drive, yellow=(-50, -45, 900), blue=(-50, -50, 850), red=(-50, -50, 850), green=(-50, -50, 850))
    # grab cube
    servo.move(Wrist.CUBE1, 1)
    servo.move(Arm.CUBE1, 1)
    servo.move(Claw.CLOSED, 1, 3)
    msleep(500)
    servo.move(Arm.HIGHEST, 1)
    servo.move(Wrist.HIGH, 1)
    ROBOT.run(drive, yellow=(-25, -25, 450), blue=(0, 0, 0), red=(0, 0, 0), green=(0, 0, 0))


def go_to_analysis_lab4():
    print("analysis lab 4")
    gyro_turn(-40, 40, 81)
    ROBOT.run(drive, yellow=(40, 40, 3500), blue=(60, 60, 2200), red=(60, 60, 2200), green=(60, 60, 2200))
    square_up_tophats(40, 40)  # yellow is 42, 40
    square_up_white(-5, -5)
    ROBOT.run(drive, yellow=(25, 25, 1850), blue=(25, 25, 1850), red=(25, 25, 1850), green=(25, 25, 1850))
    gyro_turn(-40, 40, 81)
    cube_down()
    drive(-25, -25, 500)


def cube_down():
    square_up_tophats(15, 15)
    if look_for_third_cube():
        place_fourth_cube()
    elif look_for_second_cube():
        place_third_cube()
    else:
        place_second_cube()


def place_fourth_cube():
    square_up_white(-5, -5)
    drive(-25, -25, 825)
    msleep(100)
    servo.move(Wrist.CUBE4_DOWN, 1)
    msleep(100)
    servo.move(Arm.CUBE4_DOWN, 1)
    msleep(250)
    servo.move(Claw.OPEN, 1)

    # TODO: Change code for red robot 2nd cube delivery, we didn't finish it today 4/21/23
