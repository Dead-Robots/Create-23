from typing import Optional

from createserial.encoders import Encoders
from createserial.constants import Opcode
from createserial.serial import query_create
from kipr import msleep, disable_servos, enable_servos
import servo
from common.gyro_movements import gyro_init, gyro_turn, straight_drive_distance, calibrate_straight_drive_distance
from utilities import wait_for_button
from constants.servos import Claw, Wrist, Arm, translate_arm, translate_claw
from constants import ports
from drive import drive, untimed_drive, square_up_tophats, square_up_white, stop_motors, straight_drive_black
from common import ROBOT, light, post
from sensors import on_black_left, look_for_second_cube, look_for_third_cube, test_et
from createserial.shutdown import shutdown_create_in

encoders: Optional[Encoders] = None


def init():
    # print('Press button to calibrate gyro, do not move robot.')
    # wait_for_button("press button to cal gyros, DO NOT MOVE ROBOT!")
    # msleep(1000)
    enable_servos()
    if ROBOT.is_red:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 1.0, 0.094, 0.04, 0.7, 0.0)
    elif ROBOT.is_green:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.983, 0.094, 0.1, 0.3, 0.0)
    else:
        raise Exception("Set up this color plz")
    global encoders
    encoders = Encoders()
    post.post_core(servo_test, test_motor, test_sensors, calibration_function=calibrate)
    # wait_for_button()
    # gyro_turn(-40, 40, 180)
    # wait_for_button()
    # print('Calibration Complete')


def calibrate():
    calibrate_straight_drive_distance(11.5, direction=-1, speed=20)


def servo_test():
    servo.move(Arm.NINETY, 1)
    # servo.move(Wrist.ZERO, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    # servo.move(Wrist.PUSH_RINGS, 1)
    square_up_tophats(15, 15)
    square_up_white(-15, -15)
    servo.move(Arm.ONE_THIRTY_EIGHT, 1)
    wait_for_button("End of self test, press button to continue run.")


def test_motor():
    pass


def test_sensors():
    pass


def square_up_rings():
    square_up_tophats(35, 30)
    square_up_white(-15, -15)


def get_red_ring():
    # square up on black line
    square_up_rings()
    # turn 90 degrees to get red ring
    gyro_turn(40, -40, 90)
    # put arm into position to get the red ring
    servo.move(Arm.RED_RING, 1)
    # put claw into position to get the red ring
    servo.move(Claw.OPEN, 1)
    # drive forwards to get the ring
    straight_drive_distance(70, 20)
    msleep(500)
    # pick up red ring
    servo.move(Claw.RED_RING, 1)
    msleep(500)
    # put arm into position to deliver the red ring
    servo.move(Arm.DELIVER_RED_RING, 1)


def deliver_red_ring():
    # back up after grabbing the red ring
    straight_drive_distance(-70, 14)
    # turn towards the cube
    gyro_turn(-50, 50, 90)
    # drive until the cube goes over the edge
    straight_drive_distance(70, 26)
    # raise arm to release the cube
    servo.move(Arm.RED_RING_2, 1)
    # back up
    straight_drive_distance(-70, 4)
    # lower arm back down
    servo.move(Arm.RED_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    # back up to get the yellow ring
    straight_drive_distance(-70, 20)
    # square up to get into a repeatable position
    square_up_rings()


def get_orange_ring():
    # turn to get orange ring
    gyro_turn(50, -50, 90)
    # put arm in position to get the orange ring
    servo.move(Arm.ORANGE_RING, 1)
    # put claw in position to get orange ring
    servo.move(Claw.OPEN, 1)
    # drive forwards
    straight_drive_distance(60, 16)
    # put claw in position to get orange ring
    servo.move(Claw.YELLOW_RING, 1)
    # put arm in position to get orange ring
    servo.move(Arm.ORANGE_RING, 1)
    # raise arm
    servo.move(Arm.DELIVER_RED_RING, 1)


def deliver_orange_ring():
    # lift arm straight up
    servo.move(Arm.ZERO, 1)
    # turn 90 degrees left
    gyro_turn(-50, 50, 90)
    # square up
    square_up_white(15, 15)
    # drive straight
    straight_drive_distance(65, 8)
    # turn 90 degrees right
    gyro_turn(50, -50, 90)
    # drive until black line
    straight_drive_black(40)
    # square up on black
    square_up_tophats(15, 15)
    # square up on white
    square_up_white(-15, -15)
    # straight drive down to the last cube
    straight_drive_distance(65, 37)
    # turn towards the cube
    gyro_turn(-50, 50, 90)
    # put arm into position
    servo.move(Arm.DELIVER_RED_RING, 1)
    # drive until the cube goes over the edge
    straight_drive_distance(65, 17)
    # raise arm to release the cube
    servo.move(Arm.RED_RING_2, 1)
    # back up
    straight_drive_distance(-80, 4)
    # lower arm back down
    servo.move(Arm.RED_RING_DOWN, 1)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    # back up so we don't break
    straight_drive_distance(-80, 7)
    # turn 90 degrees left
    gyro_turn(-50, 50, 90)
    # square up on black
    straight_drive_black(80)
    # drive towards yellow ring
    straight_drive_distance(65, 28)
    # turn 90 degrees left
    gyro_turn(-50, 50, 90)
    # square up on the black line
    straight_drive_black(80)
    # drive straight
    straight_drive_distance(65, 2)
    # pivot on left to turn 90 degrees, towards yellow ring
    gyro_turn(0, 80, 90)


def get_yellow_ring():
    # # turn to get yellow ring
    # gyro_turn(40, -40, 90)
    # put arm in position to get the yellow ring
    servo.move(Arm.YELLOW_RING, 1)
    # put claw in position to get yellow ring
    servo.move(Claw.OPEN, 1)
    # drive forwards
    straight_drive_distance(40, 5)
    # put claw in position to get yellow ring
    servo.move(Claw.YELLOW_RING, 1)
    # put arm in position to get yellow ring
    servo.move(Arm.YELLOW_RING, 1)
    # raise arm
    servo.move(Arm.DELIVER_RED_RING, 1)


def deliver_yellow_ring():
    # lift arm straight up
    servo.move(Arm.ZERO, 1)
    # turn 90 degrees left
    gyro_turn(-50, 50, 90)
    # square up
    square_up_white(15, 15)
    # drive straight
    straight_drive_distance(65, 8)
    # turn 90 degrees right
    gyro_turn(50, -50, 90)
    # drive until black line
    straight_drive_black(80)
    # square up on black
    square_up_tophats(15, 15)
    # square up on white
    square_up_white(-15, -15)
    # pivot to face the gray tape
    gyro_turn(0, 50, 90)

    # back up so we don't break
    # straight_drive_distance(-40, 4.5)
    # # put arm down to deliver the yellow ring onto the tape
    # servo.move(Arm.YELLOW_RING_DOWN, 1)

    # # move forwards
    straight_drive_distance(65, 8)
    # open the claw to release the ring
    servo.move(Claw.OPEN, 1)
    # back up again
    straight_drive_distance(-80, 7)
    # # raise arm
    # servo.move(Arm.END_POSITION, 1)
    # turn right
    gyro_turn(50, -50, 90)
    # square up
    square_up_tophats(-15, -15)
    # drive back
    straight_drive_distance(-80, 20)
    # turn right
    gyro_turn(50, -50, 90)
    # square up
    square_up_tophats(15, 15)
    # straight drive
    straight_drive_distance(65, 9)
    # turn left
    gyro_turn(-50, 50, 90)


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
    square_up_tophats(15, 15)
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
    servo.move(Arm.GREEN_RING, 1)
    # drive towards the ring stack
    straight_drive_distance(40, 9)
    # close claw to pick up the green ring
    servo.move(Claw.YELLOW_RING, 1)
    # raise arm after picking up green ring
    servo.move(Arm.ZERO, 1)
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
    servo.move(Arm.DELIVER_RED_RING, 1)
    # turn towards the ring stack
    gyro_turn(30, -30, 90)
    # put arm into position
    servo.move(Arm.BLUE_RING, 1)
    # move forwards
    straight_drive_distance(40, 3)
    # close claw
    servo.move(Claw.YELLOW_RING, 1)
    # raise arm
    servo.move(Arm.ZERO, 1)
    # back up
    straight_drive_distance(-40, 5)


def blue_ring_left():
    # move arm
    servo.move(Arm.BLUE_RING, 1)
    # drive towards the ring stack
    straight_drive_distance(40, 9)
    # close claw to pick up the green ring
    servo.move(Claw.YELLOW_RING, 1)
    # raise arm after picking up green ring
    servo.move(Arm.DELIVER_RED_RING, 1)
    # turn left
    gyro_turn(-30, 30, 90)
    # deliver blue ring
    servo.move(Arm.YELLOW_RING_DOWN, 1)
    # move forward towards the tape
    straight_drive_distance(40, 13)
    # open claw
    servo.move(Claw.OPEN, 1)
    

def push_rings():
    # right motor is too strong
    servo.move(Claw.OPEN, 1)
    gyro_turn(30, -30, 66, True)
    servo.move(Arm.PUSH_RINGS)
    servo.move(Wrist.PUSH_RINGS)
    drive(35, 30, 1500)
    gyro_turn(0, 30, 57, True)
    drive(35, 30, 1300)
    drive(-35, -30, 700)
    # red ring grab
    servo.move(Arm.RED_RING, 1)
    servo.move(Wrist.RED_RING, 1)
    drive(35, 30, 150)
    msleep(500)
    servo.move(Claw.RED_RING, 1)
    msleep(500)
    servo.move(Arm.RING_UP, 1)
    # turn and place it down
    gyro_turn(-30, 30, 30, True)
    drive(31, 30, 1350)
    # gyro_turn(15, 0, 10, True)
    # drive(-17, -15, 1500)
    servo.move(Wrist.RING_DROP, 1)
    servo.move(Arm.RING_DROP, 1)
    gyro_turn(30, -30, 5, True)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.ONE_THIRTY_EIGHT, 1)
    servo.move(Wrist.PUSH_RINGS, 1)
    # turn and push the rings towards the other end
    gyro_turn(30, -30, 80, True)
    drive(-35, -30, 750)
    gyro_turn(30, -30, 10, True)

    # turn and raise arm for second ring, then back up
    # servo.move(Arm.ZERO, 1)
    # gyro_turn(45, -45, 90, True)
    # drive(-30, -26, 1000)
    # # put arm amd wrist in position
    # servo.move(Wrist.PUSH_RINGS, 1)
    # servo.move(Arm.PUSH_RINGS, 1)


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
    left, right = encoders.values
    return -1 * left, -1 * right


def shutdown():
    # servo.move(Arm.START, 1)
    # servo.move(Wrist.START, 1)
    # servo.move(Claw.OPEN, 1)
    msleep(1000)
    servo.move(Wrist.PUSH_RINGS, 1)
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


