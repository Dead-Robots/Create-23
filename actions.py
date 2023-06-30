from typing import Optional

from createserial.encoders import Encoders
from createserial.constants import Opcode
from createserial.serial import query_create
from kipr import msleep, disable_servos, enable_servos, motor_power
import servo
from common.gyro_movements import gyro_init, gyro_turn, straight_drive_distance, calibrate_straight_drive_distance, \
    straight_drive
from utilities import wait_for_button
from constants.servos import Claw, Arm
from drive import drive, untimed_drive, square_up_black, square_up_white, stop_motors, straight_drive_black
from common import ROBOT, light, post
from sensors import test_et
from createserial.shutdown import shutdown_create_in

encoders: Optional[Encoders] = None


def init():
    motor_power(3, 100)
    enable_servos()
    servo.move(Arm.REST_POSITION)
    servo.move(Claw.CLOSED)
    if ROBOT.is_red:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.95, 0.11, 0.04, 0.7, 0.0)
    elif ROBOT.is_green:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.990, 0.095, 0.1, 0.3, 0.0)
    else:
        raise Exception("This robot is not set up to use gyro_init located in main, please set this color up.")
    global encoders
    encoders = Encoders()
    post.post_core(servo_test, test_motor, test_sensors, calibration_function=calibrate)


def calibrate():
    calibrate_straight_drive_distance(11.5, direction=-1, speed=20)


def servo_test():
    servo.move(Arm.NINETY, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    square_up_black(15, 15)
    square_up_white(-15, -15)
    servo.move(Arm.REST_POSITION, 1)
    servo.move(Claw.CLOSED, 1)


def test_motor():
    pass


def test_sensors():
    pass


def get_red_ring():
    servo.move(Arm.DRIVING_RELAXED, 1)
    gyro_turn(40, 0, 60, False)
    square_up_black(25, 25)
    square_up_white(20, 20)
    gyro_turn(-20, 20, 7)
    servo.move(Claw.OPEN, 0)
    servo.move(Arm.RED_RING_PICKUP, 1)
    straight_drive_distance(30, 15)
    servo.move(Claw.RED_RING, 1)
    servo.move(Arm.DELIVER_SHORT_RING, 1)


def deliver_red_ring():
    # back up after grabbing the red ring
    straight_drive_distance(-40, 17)
    # turn towards the cube
    gyro_turn(-40, 40, 75)
    # drive until the cube goes over the edge
    straight_drive_distance(40, 28, False)
    stop_motors()
    msleep(200)
    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1)
    # back up
    straight_drive_distance(-30, 4)
    # lower arm back down
    servo.move(Arm.SHORT_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)

    straight_drive_distance(-20, 4)


def square_up_rings():
    square_up_black(35, 30)
    square_up_white(-15, -15)


def get_orange_ring():
    gyro_turn(30, -30, 89)
    straight_drive_distance(30, 1.5, False)
    straight_drive_distance(70, 24, False)
    straight_drive_black(30)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    straight_drive_distance(-30, 3)
    gyro_turn(40, -40, 90)
    # straight_drive_black(10)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    stop_motors()
    straight_drive_distance(-30, 5)
    gyro_turn(-25, 25, 33)
    straight_drive_distance(-30, 2)
    servo.move(Arm.ORANGE_RING_PICKUP, 1)
    msleep(500)
    straight_drive_distance(30, 2, False)
    straight_drive_distance(10, 2)
    servo.move(Claw.CLOSED, 0)
    msleep(200)


def deliver_orange_ring():
    servo.move(Arm.DELIVER_SHORT_RING, 1)
    gyro_turn(-25, 25, 66)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    gyro_turn(20, 0, 3)
    straight_drive_distance(20, 0.5, False)
    straight_drive_distance(40, 1, False)
    straight_drive_distance(60, 2, False)
    straight_drive_distance(80, 22.5, False)
    straight_drive_distance(60, 2, False)
    straight_drive_distance(40, 2, False)
    straight_drive_distance(20, 1)
    gyro_turn(-30, 30, 92)
    straight_drive_distance(40, 10, False)
    stop_motors()
    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1)
    # back up
    straight_drive_distance(-30, 4.5)
    # lower arm back down
    servo.move(Arm.SHORT_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.STRAIGHT_UP, 1)
    straight_drive_distance(-40, 4)


def get_yellow_ring():
    gyro_turn(-30, 30, 93)
    straight_drive_distance(30, 2, False)
    straight_drive_distance(70, 20, False)
    straight_drive_black(30)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    stop_motors()
    gyro_turn(-25, 25, 67)
    # put arm into position to grab ring
    straight_drive_distance(-30, 2)
    servo.move(Arm.YELLOW_RING_PICKUP, 1)
    straight_drive_distance(30, 4)
    # grab ring
    servo.move(Claw.YELLOW_RING, 1)
    straight_drive_distance(-20, 3)


def deliver_yellow_ring():
    servo.move(Arm.TALL_RING_DELIVERY, 1)
    gyro_turn(20, -20, 5, False)
    gyro_turn(40, -40, 65)
    straight_drive_black(10)
    square_up_white(-5, -5)
    square_up_black(5, 5)
    square_up_white(-4, -4)
    square_up_black(4, 4)
    straight_drive_distance(30, 6.1)
    gyro_turn(40, -40, 94, True)
    # drive towards botgal and square up
    straight_drive_distance(30, 7)
    # drive(30, 30, 1450)
    servo.move(Arm.YELLOW_RING_DELIVERY, 1)
    straight_drive_distance(30, 8)
    # straight_drive_distance(-15, 1, False)
    # deliver botgal
    straight_drive_distance(-20, 1)
    servo.move(Claw.OPEN, 1)
    msleep(500)
    # put arm all the way up
    servo.move(Arm.STRAIGHT_UP, 1)
    msleep(500)
    # drive backwards
    straight_drive_distance(-15, 9.5, False)
    stop_motors()
    msleep(200)


def green_ring(left_green):
    # move arm all the way up
    servo.move(Arm.STRAIGHT_UP, 1)
    # turn 90 degrees
    gyro_turn(-40, 40, 95)
    # back up
    straight_drive_distance(-40, 6)
    square_up_black(30, 30)
    square_up_white(-15, -15)
    # turn towards green ring
    gyro_turn(-40, 40, 65)
    # back up
    # put arm into position to grab green ring
    straight_drive_distance(-30, 2)
    servo.move(Arm.GREEN_RING_PICKUP, 1)
    # move forwards to pick up green ring
    straight_drive_distance(30, 5)
    # grab the green ring
    servo.move(Claw.YELLOW_RING, 1)
    straight_drive_distance(-30, 2)
    # move the arm up
    servo.move(Arm.TALL_RING_DELIVERY, 1)
    # back up
    straight_drive_distance(-40, 1.5)
    if left_green:
        # turn right
        gyro_turn(40, -40, 60)
        # square up on black
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)
        # move forwards
        straight_drive_distance(40, 22.5)
        # turn right towards tower
        gyro_turn(40, -40, 88)
        # move forwards
        straight_drive_distance(30, 12)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-20, 9)

        gyro_turn(40, -40, 90)
        straight_drive_distance(30, 8, False)
        straight_drive_black(30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        gyro_turn(40, -40, 76)
        straight_drive_distance(-30, 2)
        servo.move(Arm.BLUE_RING_PICKUP, 1)
        straight_drive_distance(20, 5)
        servo.move(Claw.YELLOW_RING, 1)
        straight_drive_distance(-30, 4)
        servo.move(Arm.TALL_RING_DELIVERY, 1)
        gyro_turn(-40, 40, 76)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)

        # move forwards
        straight_drive_distance(40, 16.8)
        # turn left towards tower
        gyro_turn(-40, 40, 91)
        # move forwards
        straight_drive_distance(30, 12)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-20, 9)
    else:
        # turn left
        gyro_turn(-40, 40, 120)
        # drive back past the black line
        straight_drive_black(-30, False)
        straight_drive_distance(-30, 4)
        # square up on black
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)
        # move forwards
        straight_drive_distance(40, 16.8)
        # turn left towards tower
        gyro_turn(-40, 40, 91)
        # move forwards
        straight_drive_distance(30, 12)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-20, 9)

        gyro_turn(-40, 40, 90)
        straight_drive_distance(30, 8, False)
        straight_drive_black(30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        gyro_turn(-40, 40, 70)
        straight_drive_distance(-30, 2)
        servo.move(Arm.BLUE_RING_PICKUP, 1)
        straight_drive_distance(20, 5)
        servo.move(Claw.YELLOW_RING, 1)
        straight_drive_distance(-30, 4)
        servo.move(Arm.TALL_RING_DELIVERY, 1)
        gyro_turn(40, -40, 70)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)

        # move forwards
        straight_drive_distance(40, 22.5)
        # turn right towards tower
        gyro_turn(40, -40, 88)
        # move forwards
        straight_drive_distance(30, 12)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-20, 9)


def blue_ring(left_green):
    gyro_turn(-40, 40, 90)
    # square up
    square_up_white(15, 15)
    # drive straight
    straight_drive_distance(40, 12)
    # turn 90 degrees right
    gyro_turn(40, -40, 90)
    # drive until black line
    straight_drive_black(40)
    # square up on black
    square_up_black(15, 15)
    # square up on white
    square_up_white(-15, -15)
    # drive towards gray tape to place the blue ring
    straight_drive_distance(40, 22)
    # rotate towards the gray tape
    gyro_turn(-40, 40, 90)
    # move forwards
    straight_drive_distance(40, 12)
    # open claw
    servo.move(Claw.OPEN, 1)
    msleep(500)
    # back up to prevent from damaging claw
    straight_drive_distance(-40, 10)
    # move arm
    servo.move(Arm.BLUE_RING_PICKUP, 1)
    # drive towards the ring stack
    straight_drive_distance(40, 9)
    # close claw to pick up the green ring
    servo.move(Claw.YELLOW_RING, 1)
    # deliver blue ring
    servo.move(Arm.TALL_RING_DELIVERY, 1)
    # turn left
    gyro_turn(-30, 30, 90)
    if left_green:
        # move forward towards the tape
        straight_drive_distance(40, 13)
        # open claw
        servo.move(Claw.OPEN, 1)


def get_bumps():
    data = query_create([Opcode.QUERY_LIST, 1, 7], 1)
    return data != b'\x00'


def get_encoder_values():
    left, right = encoders.values
    return -1 * left, -1 * right


def shutdown():
    # servo.move(Arm.START, 1)
    # servo.move(Claw.OPEN, 1)
    msleep(500)
    servo.move(Arm.REST_POSITION, 1)
    disable_servos()


# start box position
def start_position():
    enable_servos()
    servo.move(Claw.OPEN, 1)
    wait_for_button(Arm.STRAIGHT_UP)
    servo.move(Arm.START, 1)
    light.wait_4_light(2)
    shutdown_create_in(119)


def end_position():
    servo.move(Arm.START, 1)
    servo.move(Claw.OPEN, 1)
    print('done with program')


def wait(duration):
    msleep(100)
    drive(0, 0, duration - 200)
    msleep(100)
    print('waiting')


def drive_until_bump(speed):
    straight_drive(speed, get_bumps, condition_is=False)
