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
    wait_for_button("End of self test, press button to continue to options.")


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
    straight_drive_distance(30, 15.5)
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

    # # back up to get the orange ring
    # straight_drive_distance(-50, 10)
    # # square up to get into a repeatable position
    # square_up_black(-30, -30)
    # square_up_white(15, 15)


def square_up_rings():
    square_up_black(35, 30)
    square_up_white(-15, -15)


def get_orange_ring():
    gyro_turn(30, -30, 89)
    straight_drive_distance(30, 1.5, False)
    straight_drive_distance(70, 24, False)
    straight_drive_black(30)
    square_up_rings()
    stop_motors()
    gyro_turn(25, -25, 72)
    servo.move(Arm.ORANGE_RING_PICKUP, 1)
    msleep(200)
    straight_drive_distance(30, 2)
    servo.move(Claw.CLOSED, 0)
    msleep(200)

    # straight_drive_distance(20, 2)
    # # turn to get orange ring
    # gyro_turn(30, -30, 90)
    # # put arm in position to get the orange ring
    # servo.move(Arm.ORANGE_RING_PICKUP, 1)
    # # put claw in position to get orange ring
    # servo.move(Claw.OPEN, 1)
    # # drive forwards
    # straight_drive_distance(60, 19)
    # # put claw in position to get orange ring
    # servo.move(Claw.YELLOW_RING, 1)
    # # put arm in position to get orange ring
    # servo.move(Arm.ORANGE_RING_PICKUP, 1)
    # # raise arm
    # servo.move(Arm.DELIVER_SHORT_RING, 1)


def deliver_orange_ring():
    servo.move(Arm.DELIVER_SHORT_RING, 1)
    gyro_turn(-25, 25, 72)
    square_up_rings()
    gyro_turn(20, 0, 3)
    straight_drive_distance(20, 0.5, False)
    straight_drive_distance(40, 1, False)
    straight_drive_distance(60, 2, False)
    straight_drive_distance(80, 22.5, False)
    straight_drive_distance(60, 2, False)
    straight_drive_distance(40, 2, False)
    straight_drive_distance(20, 1)
    gyro_turn(-30, 30, 92)
    straight_drive_distance(40, 12, False)
    stop_motors()

    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1)
    # back up
    straight_drive_distance(-30, 3)
    # lower arm back down
    servo.move(Arm.SHORT_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)

    straight_drive_distance(-40, 5)

    # # lift arm straight up
    # servo.move(Arm.STRAIGHT_UP, 1)
    # # turn 90 degrees left
    # gyro_turn(-50, 50, 90)
    # # square up
    # square_up_white(15, 15)
    # # drive straight
    # straight_drive_distance(30, 8)
    # # turn 90 degrees right
    # gyro_turn(50, -50, 90)
    # # drive until black line
    # straight_drive_black(40)
    # # square up on black
    # square_up_black(15, 15)
    # # square up on white
    # square_up_white(-15, -15)
    # # straight drive down to the last cube
    # straight_drive_distance(30, 32)
    # # turn towards the cube
    # gyro_turn(-50, 50, 90)
    # straight_drive_distance(-30, 8)
    # wait_for_button()
    # # put arm into position
    # servo.move(Arm.DELIVER_SHORT_RING, 1)
    # # drive until the cube goes over the edge
    # straight_drive_distance(30, 17)
    # # raise arm to release the cube
    # servo.move(Arm.SHORT_RING_UP, 1)
    # # back up
    # straight_drive_distance(-30, 4)
    # # lower arm back down
    # servo.move(Arm.SHORT_RING_DOWN, 1)
    # # drop ring on tower
    # servo.move(Claw.OPEN, 1)
    # wait_for_button()
    # # back up so we don't break... opps :p
    # straight_drive_distance(-30, 7)
    # wait_for_button("1")
    # # turn 90 degrees left
    # gyro_turn(-50, 50, 90)
    # servo.move(Arm.STRAIGHT_UP)
    # wait_for_button("2")
    # # square up on black
    # straight_drive_black(30)
    # square_up_white(20, 20)
    # wait_for_button()
    # straight_drive_distance(20, 4)
    # wait_for_button()
    # gyro_turn(-30, 30, 90)
    # wait_for_button("'Grabbing'")
    # drive_until_bump(-30)
    # wait_for_button("did the bump work? prob not")
    # servo.move(Claw.OPEN)
    # wait(250)
    # servo.move(Arm.YELLOW_RING_PICKUP)
    # wait(250)
    # gyro_turn(30, -30, 180)


def get_yellow_ring():
    gyro_turn(-30, 30, 93)
    straight_drive_distance(30, 2, False)
    straight_drive_distance(70, 20, False)
    straight_drive_black(30)
    square_up_rings()
    stop_motors()
    gyro_turn(-25, 25, 65)
    servo.move(Arm.YELLOW_RING_PICKUP, 1)
    straight_drive_distance(30, 3)
    servo.move(Claw.YELLOW_RING, 1)
    straight_drive_distance(-20, 1.5)

    # gyro_turn(-30, 30, 90)
    # wait_for_button(" 'Grabbing' ")
    # gyro_turn(30, -30, 180)
    #
    # # put arm in position to get the yellow ring
    # servo.move(Arm.YELLOW_RING_PICKUP, 1)
    # # put claw in position to get yellow ring
    # servo.move(Claw.OPEN, 1)
    # # drive forwards
    # straight_drive_distance(40, 5)
    # # put claw in position to get yellow ring
    # servo.move(Claw.YELLOW_RING, 1)
    # # put arm in position to get yellow ring
    # servo.move(Arm.YELLOW_RING_PICKUP, 1)
    # # raise arm
    # servo.move(Arm.DELIVER_SHORT_RING, 1)


def deliver_yellow_ring():
    servo.move(Arm.TALL_RING_DELIVERY)
    gyro_turn(20, -20, 5, False)
    gyro_turn(40, -40, 5, False)
    gyro_turn(60, -60, 124, False)
    gyro_turn(40, -40, 5, False)
    gyro_turn(20, -20, 5)
    straight_drive_distance(30, 19, False)
    stop_motors()
    servo.move(Claw.OPEN, 1)
    msleep(500)
    straight_drive_distance(-5, 12, False)
    stop_motors()
    msleep(200)

    # # lift arm straight up
    # servo.move(Arm.STRAIGHT_UP, 1)
    # # turn 90 degrees left
    # gyro_turn(-50, 50, 90)
    # # square up
    # square_up_white(15, 15)
    # # drive straight
    # straight_drive_distance(30, 8)
    # # turn 90 degrees right
    # gyro_turn(50, -50, 90)
    # # drive until black line
    # straight_drive_black(80)
    # # square up on black
    # square_up_black(15, 15)
    # # square up on white
    # square_up_white(-15, -15)
    # # pivot to face the gray tape
    # gyro_turn(0, 50, 90)
    #
    # # back up so we don't break
    # # straight_drive_distance(-40, 4.5)
    # # put arm down to deliver the yellow ring onto the tape
    # # servo.move(Arm.YELLOW_RING_DOWN, 1)
    #
    # # move forwards
    # straight_drive_distance(30, 8)
    # # open the claw to release the ring
    # servo.move(Claw.OPEN, 1)
    # # back up again
    # straight_drive_distance(-30, 7)
    # # raise arm
    # # servo.move(Arm.END_POSITION, 1)
    # # turn right
    # gyro_turn(50, -50, 90)
    # # square up
    # square_up_black(-15, -15)
    # # drive back
    # straight_drive_distance(-30, 20)
    # # turn right
    # gyro_turn(50, -50, 90)
    # # square up
    # square_up_black(15, 15)
    # # straight drive
    # straight_drive_distance(30, 9)
    # # turn left
    # gyro_turn(-50, 50, 90)


def blue_ring_right():
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
    # back up to prevent from damaging claw
    straight_drive_distance(-40, 10)


def green_ring_left():
    # move arm
    servo.move(Arm.GREEN_RING_PICKUP, 1)
    # drive towards the ring stack
    straight_drive_distance(40, 9)
    # close claw to pick up the green ring
    servo.move(Claw.YELLOW_RING, 1)
    # raise arm after picking up green ring
    servo.move(Arm.STRAIGHT_UP, 1)
    # back up a little bit
    straight_drive_distance(-40, 0.5)
    # turn left
    gyro_turn(-30, 30, 90)
    # deliver green ring??
    # servo.move(Arm.YELLOW_RING_DOWN, 1)
    # move forward towards the tape
    straight_drive_distance(40, 24)
    # open claw
    servo.move(Claw.OPEN, 1)
    # COPY AND PASTE INTO GREEN RING RIGHT WHEN YOU MAKE THE FUNCTION
    # move backwards to get the blue ring
    straight_drive_distance(-40, 24)
    # bring arm up
    servo.move(Arm.DELIVER_SHORT_RING, 1)
    # turn towards the ring stack
    gyro_turn(30, -30, 90)
    # put arm into position
    servo.move(Arm.BLUE_RING_PICKUP, 1)
    # move forwards
    straight_drive_distance(40, 3)
    # close claw
    servo.move(Claw.YELLOW_RING, 1)
    # raise arm
    servo.move(Arm.STRAIGHT_UP, 1)
    # back up
    straight_drive_distance(-40, 5)


def blue_ring_left():
    # move arm
    servo.move(Arm.BLUE_RING_PICKUP, 1)
    # drive towards the ring stack
    straight_drive_distance(40, 9)
    # close claw to pick up the green ring
    servo.move(Claw.YELLOW_RING, 1)
    # raise arm after picking up green ring
    servo.move(Arm.DELIVER_SHORT_RING, 1)
    # turn left
    gyro_turn(-30, 30, 90)
    # deliver blue ring
    servo.move(Arm.TALL_RING_DELIVERY, 1)
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
