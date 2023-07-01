from time import sleep
from typing import Optional

from createserial.encoders import Encoders
from createserial.constants import Opcode
from createserial.serial import query_create
from kipr import disable_servos, enable_servos, motor_power, clear_motor_position_counter
import servo
from common.gyro_movements import gyro_init, gyro_turn, straight_drive_distance, calibrate_straight_drive_distance, \
    straight_drive
from common.multitasker import MultitaskedMotor
from constants.ports import RAKE
from utilities import wait_for_button
from constants.servos import Claw, Arm
from drive import drive, untimed_drive, square_up_black, square_up_white, stop_motors, straight_drive_black
from common import ROBOT, light, post
from sensors import test_et
from createserial.shutdown import shutdown_create_in

rake_manager = None
encoders: Optional[Encoders] = None


def msleep(milliseconds):
    sleep(milliseconds/1000)


def init():
    post.post_core(servo_test, test_motor, test_sensors, initial_setup, calibration_function=calibrate)


def calibrate():
    calibrate_straight_drive_distance(11.5, direction=-1, speed=20)


def initial_setup():
    if ROBOT.is_red:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.95, 0.11, 0.04, 0.7, 0.0)
    elif ROBOT.is_green:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.990, 0.095, 0.1, 0.3, 0.0)
    else:
        raise Exception("This robot is not set up to use gyro_init located in main, please set this color up.")
    print("Gyro calibration complete.")
    motor_power(3, 100)
    enable_servos()
    servo.move(Arm.DRIVING_RELAXED, 1)
    servo.move(Claw.CLOSED, 0)
    servo.move(Arm.START, 1)
    global encoders
    encoders = Encoders()
    motor_power(RAKE, -50)
    msleep(1500)
    motor_power(RAKE, -20)
    msleep(1000)
    clear_motor_position_counter(RAKE)
    global rake_manager
    # light.wait_4_light(2)
    # shutdown_create_in(119)
    rake_manager = MultitaskedMotor(RAKE, 50)


def servo_test():
    servo.move(Arm.NINETY, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.START, 1)
    servo.move(Claw.CLOSED, 1)


def test_motor():
    rake_manager.position = 800
    msleep(1000)
    rake_manager.position = 400
    msleep(1000)
    rake_manager.position = 800
    msleep(1000)
    rake_manager.position = 0
    msleep(1000)


def test_sensors():
    square_up_black(15, 15)
    square_up_white(-15, -15)


def get_red_ring():
    rake_manager.position = 400
    servo.move(Arm.DRIVING_RELAXED, 1)
    gyro_turn(40, 0, 5, False)
    gyro_turn(60, 0, 49, False)
    gyro_turn(40, 0, 5, False)
    square_up_black(25, 25)
    square_up_white(-10, -10)
    square_up_black(10, 10)
    square_up_white(20, 20)
    stop_motors(300)
    gyro_turn(-20, 20, 7, False)
    stop_motors(300)
    servo.move(Claw.OPEN, 0)
    servo.move(Arm.RED_RING_PICKUP, 1)
    straight_drive_distance(50, 14.5, False)
    stop_motors(600)
    servo.move(Claw.CLOSED, 0)
    servo.move(Arm.DELIVER_SHORT_RING, 1)


def deliver_red_ring():
    # back up after grabbing the red ring
    straight_drive_distance(-50, 16.5, False)
    stop_motors(300)
    # turn towards the cube
    gyro_turn(-40, 40, 77, False)
    stop_motors(300)
    # drive until the cube goes over the edge
    straight_drive_distance(40, 2, False)
    straight_drive_distance(60, 20, False)
    straight_drive_distance(40, 6, False)
    # move the encryption key arm into place
    rake_manager.position = 200
    stop_motors(300)
    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1)
    # back up and pull encryption key
    straight_drive_distance(-40, 3.5, False)
    rake_manager.position = 900
    stop_motors(200)
    straight_drive_distance(-20, 0.5, False)
    stop_motors(200)
    # lower arm for delivery
    servo.move(Arm.SHORT_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    # back away from tower
    straight_drive_distance(-40, 4, False)
    stop_motors(600)


def get_orange_ring():
    gyro_turn(40, -40, 85, False)
    stop_motors(600)
    straight_drive_distance(30, 1.5, False)
    straight_drive_distance(70, 24, False)
    straight_drive_black(40, False)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    square_up_black(5, 5)
    gyro_turn(30, -30, 72, False)
    stop_motors(300)
    straight_drive_distance(-40, 3, False)
    stop_motors(300)
    servo.move(Arm.ORANGE_RING_PICKUP, 1)
    msleep(200)
    straight_drive_distance(30, 5, False)
    stop_motors(200)
    servo.move(Claw.CLOSED, 0)
    msleep(200)


def deliver_orange_ring():
    servo.move(Arm.DELIVER_SHORT_RING, 1)
    straight_drive_distance(-30, 2.5)
    gyro_turn(-30, 30, 70, False)
    stop_motors(300)
    square_up_white(-20, -20)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    square_up_black(10, 10)
    square_up_white(-6, -6)
    gyro_turn(20, 0, 3, False)
    stop_motors(200)
    straight_drive_distance(40, 1, False)
    straight_drive_distance(60, 2, False)
    straight_drive_distance(80.5, 22, False)
    straight_drive_distance(60, 2, False)
    straight_drive_distance(40, 2, False)
    straight_drive_distance(20, 1, False)
    stop_motors(200)
    gyro_turn(-40, 40, 92, False)
    stop_motors(400)
    straight_drive_distance(40, 12, False)
    stop_motors()
    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1)
    rake_manager.position = 300
    # back up
    straight_drive_distance(-30, 4.8, False)
    rake_manager.position = 900
    stop_motors(200)
    # lower arm back down
    servo.move(Arm.SHORT_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    straight_drive_distance(-40, 4.2, False)
    stop_motors(300)


def get_yellow_ring():
    gyro_turn(-40, 40, 90, False)
    stop_motors(300)
    straight_drive_distance(40, 2, False)
    straight_drive_distance(70, 16, False)
    straight_drive_black(30, False)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    stop_motors(200)
    gyro_turn(-40, 40, 69, False)
    stop_motors(200)
    # put arm into position to grab ring
    straight_drive_distance(-40, 2, False)
    stop_motors(200)
    servo.move(Arm.YELLOW_RING_PICKUP, 1)
    straight_drive_distance(30, 4.5, False)
    # grab ring
    stop_motors(200)
    servo.move(Claw.YELLOW_RING, 0)
    straight_drive_distance(-30, 3.5, False)
    stop_motors(200)


def deliver_yellow_ring():
    servo.move(Arm.TALL_RING_DELIVERY, 1)
    gyro_turn(20, -20, 5, False)
    gyro_turn(40, -40, 67, False)
    stop_motors(300)
    straight_drive_distance(-40, 1, False)
    square_up_black(30, 30)
    square_up_white(-10, -10)
    msleep(500)
    square_up_black(8, 8)
    square_up_white(-6, -6)
    square_up_black(4, 4)
    straight_drive_distance(40, 6.1, False)
    stop_motors(300)
    gyro_turn(40, -40, 92, False)
    stop_motors(300)
    # drive towards botgal and square up
    straight_drive_distance(40, 7, False)
    # drive(30, 30, 1450)
    servo.move(Arm.YELLOW_RING_DELIVERY, 1)
    straight_drive_distance(40, 8, False)
    stop_motors()
    # deliver botgal
    straight_drive_distance(-30, 1, False)
    stop_motors(300)
    servo.move(Claw.OPEN, 1)
    msleep(300)
    rake_manager.position = 500
    # put arm all the way up
    servo.move(Arm.STRAIGHT_UP, 1)
    # drive backwards
    straight_drive_distance(-15, 4.3, False)
    stop_motors()
    rake_manager.position = 900
    servo.move(Claw.CLOSED, 0)
    msleep(100)
    straight_drive_distance(40, 4.5, False)
    straight_drive_distance(-40, 1, False)
    servo.move(Claw.OPEN, 0)
    straight_drive_distance(-40, 5, False)
    stop_motors(300)


def deliver_tall_rings(left_green):
    # move arm all the way up
    servo.move(Arm.STRAIGHT_UP, 1)
    # turn 90 degrees
    gyro_turn(-40, 40, 95, False)
    stop_motors(300)
    # back up
    straight_drive_black(-40, False)
    straight_drive_distance(-40, 2.5, False)
    square_up_black(30, 30)
    square_up_white(-15, -15)
    msleep(500)
    square_up_black(10, 10)
    square_up_white(-5, -5)
    stop_motors(100)
    # turn towards green ring
    gyro_turn(-40, 40, 68, False)
    stop_motors(300)
    # back up
    straight_drive_distance(-40, 2, False)
    stop_motors(300)
    # put arm into position to grab green ring
    servo.move(Arm.GREEN_RING_PICKUP, 1)
    # move forwards to pick up green ring
    straight_drive_distance(40, 6.5, False)
    stop_motors(300)
    # grab the green ring
    servo.move(Claw.YELLOW_RING, 0)
    straight_drive_distance(-40, 2, False)
    stop_motors(300)
    # move the arm up
    servo.move(Arm.TALL_RING_DELIVERY, 1)
    # back up
    straight_drive_distance(-40, 1.5, False)
    stop_motors(300)
    if left_green:
        # turn right
        gyro_turn(40, -40, 65, False)
        stop_motors(200)
        # square up on black
        straight_drive_distance(-40, 2, False)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)
        stop_motors(100)
        # move forwards
        straight_drive_distance(40, 22.5, False)
        stop_motors(300)
        # turn right towards tower
        gyro_turn(40, -40, 88, False)
        stop_motors(300)
        # move forwards
        straight_drive_distance(40, 12, False)
        stop_motors(300)
        # open claw
        servo.move(Claw.OPEN, 1)
        rake_manager.position = 300
        # back up so we don't break
        straight_drive_distance(-20, 4.5, False)
        rake_manager.position = 900
        straight_drive_distance(-40, 3.7, False)
        stop_motors(300)

        gyro_turn(40, -40, 90, False)
        stop_motors(300)
        straight_drive_distance(50, 12, False)
        straight_drive_black(40, False)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        gyro_turn(40, -40, 74, False)
        stop_motors(300)
        straight_drive_distance(-30, 3, False)
        stop_motors(200)
        servo.move(Arm.BLUE_RING_PICKUP, 1)
        straight_drive_distance(40, 7, False)
        stop_motors(300)
        servo.move(Claw.YELLOW_RING, 0)
        straight_drive_distance(-30, 5, False)
        stop_motors(200)
        servo.move(Arm.TALL_RING_DELIVERY, 1)
        gyro_turn(-40, 40, 74, False)
        stop_motors(300)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)
        stop_motors(100)

        # move forwards
        straight_drive_distance(40, 16.8, False)
        stop_motors(300)
        # turn left towards tower
        gyro_turn(-40, 40, 91, False)
        stop_motors(300)
        # move forwards
        straight_drive_distance(40, 12, False)
        stop_motors(300)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        rake_manager.position = 500
        straight_drive_distance(-15, 5, False)
        stop_motors(100)
        rake_manager.position = 900
        straight_drive_distance(-40, 9.1, False)
        stop_motors(300)
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
        straight_drive_distance(40, 12)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-40, 9)

        gyro_turn(-40, 40, 90)
        straight_drive_distance(40, 8, False)
        straight_drive_black(30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        gyro_turn(-40, 40, 68)
        straight_drive_distance(-30, 1)
        servo.move(Arm.BLUE_RING_PICKUP, 1)
        straight_drive_distance(40, 7.5)
        servo.move(Claw.YELLOW_RING, 0)
        straight_drive_distance(-30, 4)
        servo.move(Arm.TALL_RING_DELIVERY, 1)
        gyro_turn(40, -40, 68)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)

        # move forwards
        straight_drive_distance(40, 22.5)
        # turn right towards tower
        gyro_turn(40, -40, 88)
        # move forwards
        straight_drive_distance(40, 12)
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-40, 14)


def get_bumps():
    data = query_create([Opcode.QUERY_LIST, 1, 7], 1)
    return data != b'\x00'


def get_encoder_values():
    left, right = encoders.values
    return -1 * left, -1 * right


def shutdown():
    rake_manager.running = False
    servo.move(Arm.REST_POSITION, 1)
    disable_servos()


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
