from time import sleep, time
from typing import Optional

from createserial.encoders import Encoders
from createserial.constants import Opcode
from createserial.serial import query_create
from createserial.shutdown import shutdown_create_in
from kipr import disable_servos, enable_servos, motor_power, clear_motor_position_counter, camera_close
import servo
from camera import init_camera, load_config, card_scan
from common.gyro_movements import gyro_init, gyro_turn, straight_drive_distance, calibrate_straight_drive_distance, \
    straight_drive
from common.light import wait_4_light
from common.multitasker import MultitaskedMotor
from constants.ports import RAKE, LIGHT
from constants.servos import Claw, Arm
from constants.rake import RakePositions
from drive import drive, untimed_drive, square_up_black, square_up_white, stop_motors, straight_drive_black
from common import ROBOT, post
from utilities import wait_for_button

rake_manager = None
encoders: Optional[Encoders] = None
start_time: float


def msleep(milliseconds):
    sleep(milliseconds/1000)


def rake_test():
    rake_manager.position = RakePositions.START
    wait_for_button()
    rake_manager.position = RakePositions.LOW_KEY_REST
    wait_for_button()
    rake_manager.position = RakePositions.LOW_KEY
    wait_for_button()
    rake_manager.position = RakePositions.REST
    wait_for_button()
    rake_manager.position = RakePositions.MIDDLE_KEY
    wait_for_button()
    rake_manager.position = RakePositions.REST
    wait_for_button()
    rake_manager.position = RakePositions.HIGH_KEY
    wait_for_button()
    rake_manager.position = RakePositions.REST
    wait_for_button()
    rake_manager.position = RakePositions.END


def init():
    global start_time
    post.post_core(servo_test, test_motor, test_sensors, initial_setup, calibration_function=calibrate)
    load_config()
    init_camera()
    wait_4_light(LIGHT, function=card_scan, function_every=1)
    camera_close()
    shutdown_create_in(119)
    start_time = time()


def calibrate():
    rake_manager.position = RakePositions.REST
    servo.move(Arm.STRAIGHT_UP, 1)
    wait_for_button("Press button to begin drive distance calibration.")
    calibrate_straight_drive_distance(11.5, direction=-1, speed=20)


def initial_setup():
    if ROBOT.is_red:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.99, 0.07, 0.03, 0.9, 0.0)
    elif ROBOT.is_green:
        gyro_init(untimed_drive, stop_motors, get_encoder_values, get_bumps, 0.99, 0.095, 0.1, 0.3, 0.0)
    else:
        raise Exception("This robot is not set up to use gyro_init located in main, please set this color up.")
    print("Gyro calibration complete.")
    motor_power(3, 100)
    enable_servos()
    motor_power(RAKE, -40)
    msleep(1500)
    motor_power(RAKE, 0)
    servo.move(Arm.DRIVING_RELAXED, 1)
    servo.move(Claw.CLOSED, 0)
    servo.move(Arm.START, 1)
    motor_power(RAKE, -15)
    msleep(500)
    global encoders
    encoders = Encoders()
    clear_motor_position_counter(RAKE)
    global rake_manager
    rake_manager = MultitaskedMotor(RAKE, RakePositions.START)


def servo_test():
    servo.move(Arm.NINETY, 1)
    servo.move(Claw.CLOSED, 1)
    servo.move(Claw.OPEN, 1)
    servo.move(Arm.DRIVING_RELAXED, 1)
    servo.move(Claw.CLOSED, 1)


def test_motor():
    rake_manager.position = RakePositions.POST_HIGH
    msleep(1000)
    rake_manager.position = RakePositions.POST_LOW
    msleep(1000)
    rake_manager.position = RakePositions.START
    msleep(1000)


def test_sensors():
    square_up_black(15, 15)
    square_up_white(-15, -15)
    servo.move(Arm.START, 1)


def get_red_ring():
    rake_manager.position = RakePositions.LOW_KEY_REST
    servo.move(Arm.DRIVING_RELAXED, 1, 2)
    msleep(200)
    gyro_turn(40, 0, 5, False)
    gyro_turn(70, 0, 49, False)
    gyro_turn(40, 0, 5, False)
    square_up_black(25, 25)
    square_up_white(-10, -10)
    square_up_black(10, 10)
    square_up_white(20, 20)
    stop_motors(100)
    ROBOT.run(gyro_turn, red=(-20, 20, 10, False), green=(-20, 20, 7, False))
    stop_motors()
    servo.move(Arm.RED_RING_PICKUP, 1, 2)
    servo.move(Claw.OPEN, 0)
    msleep(200)
    straight_drive_distance(50, 14, False)
    stop_motors(500)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when grabbing red ring.")
    servo.move(Claw.CLOSED, 0)
    servo.move(Arm.DELIVER_SHORT_RING, 1, 2)
    msleep(200)


def deliver_red_ring():
    # back up after grabbing the red ring
    ROBOT.run(straight_drive_distance, red=(-50, 16.3, False), green=(-50, 16.5, False))
    stop_motors(200)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when arriving at red tower.")
    # turn towards the cube
    ROBOT.run(gyro_turn, red=(-40, 40, 74, False), green=(-40, 40, 74, False))
    stop_motors(200)
    # drive until the cube goes over the edge
    straight_drive_distance(40, 2, False)
    ROBOT.run(straight_drive_distance, red=(70, 24.5, False), green=(70, 22, False))
    straight_drive_distance(40, 3, False)
    # move the encryption key arm into place
    rake_manager.position = RakePositions.LOW_KEY
    stop_motors()
    print(str(round(time()-start_time, 2)) + " seconds elapsed when delivering red ring.")
    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1, 2)
    msleep(200)
    # back up and pull encryption key
    straight_drive_distance(-40, 0.5, False)
    rake_manager.position = RakePositions.LOW_KEY_PULL
    straight_drive_distance(-40, 3.5, False)
    stop_motors()
    # lower arm for delivery
    servo.move(Arm.SHORT_RING_DOWN, 1, 2)
    rake_manager.position = RakePositions.REST
    msleep(200)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    # back away from tower
    ROBOT.run(straight_drive_distance, red=(-40, 4, False), green=(-40, 4.3, False))
    print(str(round(time()-start_time, 2)) + " seconds elapsed when leaving red tower.")
    stop_motors(300)


def get_orange_ring():
    ROBOT.run(gyro_turn, red=(40, -40, 89.5, False), green=(40, -40, 86, False))
    stop_motors(200)
    straight_drive_distance(30, 1.5, False)
    straight_drive_distance(70, 25, False)
    straight_drive_black(40, False)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when squaring up to get orange ring.")
    square_up_black(20, 20)
    square_up_white(-10, -10)
    square_up_black(5, 5)
    stop_motors(100)

    straight_drive_distance(-40, 3, False)
    stop_motors(200)
    gyro_turn(40, -40, 90, False)
    stop_motors(200)
    square_up_black(40, 40)
    square_up_white(-15, -15)
    stop_motors(100)
    straight_drive_distance(-30, 5, False)
    stop_motors(200)
    ROBOT.run(gyro_turn, red=(-40, 40, 19, False), green=(-40, 40, 29, False))
    stop_motors(200)
    straight_drive_distance(-30, 2, False)
    stop_motors(500)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when grabbing orange ring.")
    servo.move(Arm.ORANGE_RING_PICKUP, 1, 2)
    msleep(200)
    straight_drive_distance(30, 4, False)
    stop_motors(400)
    servo.move(Claw.CLOSED, 0)
    msleep(100)


def deliver_orange_ring():
    servo.move(Arm.DELIVER_SHORT_RING, 1, 2)
    msleep(100)
    straight_drive_distance(-30, 0.5)
    ROBOT.run(gyro_turn, red=(-40, 40, 69, False), green=(-40, 40, 58, False))
    stop_motors(200)
    square_up_white(-20, -20)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    square_up_black(10, 10)
    square_up_white(-6, -6)
    stop_motors(200)
    gyro_turn(20, 0, 3.5, False)
    stop_motors(200)
    straight_drive_distance(40, 1, False)
    straight_drive_distance(60, 2, False)
    ROBOT.run(straight_drive_distance, red=(80, 23.4, False), green=(80, 23, False))
    straight_drive_distance(60, 2, False)
    straight_drive_distance(40, 2, False)
    straight_drive_distance(20, 1, False)
    stop_motors(200)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when arriving at orange tower.")
    ROBOT.run(gyro_turn, red=(-40, 40, 89, False), green=(-40, 40, 92, False))
    stop_motors(200)
    ROBOT.run(straight_drive_distance, red=(40, 12, False), green=(40, 11, False))
    stop_motors()
    # raise arm to release the cube
    servo.move(Arm.SHORT_RING_UP, 1, 2)
    rake_manager.position = RakePositions.MIDDLE_KEY
    print(str(round(time()-start_time, 2)) + " seconds elapsed when delivering orange ring.")
    msleep(100)
    # back up
    straight_drive_distance(-40, 0.5, False)
    rake_manager.position = RakePositions.MIDDLE_KEY_PULL
    straight_drive_distance(-40, 4.3, False)
    rake_manager.position = RakePositions.REST
    stop_motors()
    # lower arm back down
    servo.move(Arm.SHORT_RING_DOWN, 1, 2)
    msleep(100)
    # drop ring on tower
    servo.move(Claw.OPEN, 1)
    straight_drive_distance(-40, 4, False)
    stop_motors()
    servo.move(Arm.STRAIGHT_UP, 1, 2)
    msleep(400)


def get_yellow_ring():
    gyro_turn(-40, 40, 90, False)
    stop_motors(300)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when leaving orange tower.")
    straight_drive_distance(40, 2, False)
    straight_drive_distance(70, 16, False)
    straight_drive_black(30, False)
    square_up_black(20, 20)
    square_up_white(-10, -10)
    stop_motors(200)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when squaring up to get yellow ring.")
    ROBOT.run(gyro_turn, red=(-40, 40, 60, False), green=(-40, 40, 61, False))
    stop_motors(200)
    # put arm into position to grab ring
    straight_drive_distance(-40, 2, False)
    stop_motors()
    servo.move(Arm.YELLOW_RING_PICKUP, 1, 2)
    msleep(100)
    straight_drive_distance(40, 5.5, False)
    # grab ring
    stop_motors(600)
    servo.move(Claw.YELLOW_RING, 0)
    straight_drive_distance(-40, 4.5, False)
    stop_motors(200)


def deliver_yellow_ring():
    servo.move(Arm.TALL_RING_DELIVERY, 1, 2)
    msleep(100)
    gyro_turn(20, -20, 5, False)
    ROBOT.run(gyro_turn, red=(40, -40, 63, False), green=(40, -40, 64, False))
    stop_motors(200)
    square_up_black(30, 30)
    square_up_white(-12, -12)
    square_up_black(10, 10)
    square_up_white(-8, -8)
    square_up_black(6, 6)
    straight_drive_distance(40, 6.1, False)
    stop_motors(200)
    print(str(round(time()-start_time, 2)) + " seconds elapsed when lined up with yellow tower.")
    ROBOT.run(gyro_turn, red=(40, -40, 88, False), green=(40, -40, 90, False))
    stop_motors(200)
    # drive towards botgal and square up
    straight_drive_distance(40, 7, False)
    servo.move(Arm.YELLOW_RING_DELIVERY, 1, 2)
    msleep(100)
    straight_drive_distance(40, 5, False)
    stop_motors()
    # deliver botgal
    straight_drive_distance(-30, 3, False)
    stop_motors(200)
    straight_drive_distance(30, 3.2, False)
    stop_motors(200)
    straight_drive_distance(-30, 3, False)
    stop_motors(200)
    straight_drive_distance(30, 3.2, False)
    stop_motors(600)
    straight_drive_distance(-20, 0.8, False)
    stop_motors(100)
    servo.move(Claw.OPEN, 1, 2)
    msleep(200)
    rake_manager.position = RakePositions.HIGH_KEY+130
    # put arm all the way up
    servo.move(Arm.STRAIGHT_UP, 1, 2)
    msleep(100)
    # drive backwards
    straight_drive_distance(-20, 1.4, False)
    rake_manager.position = RakePositions.HIGH_KEY_PULL
    straight_drive_distance(-20, 3.6, False)
    rake_manager.position = RakePositions.REST
    servo.move(Claw.CLOSED, 0)
    stop_motors(200)
    straight_drive_distance(20, 5.8, False)
    straight_drive_distance(-40, 6.6, False)
    servo.move(Claw.OPEN, 0)
    stop_motors(200)


def deliver_tall_rings(left_green):
    # turn 90 degrees
    gyro_turn(-40, 40, 95, False)
    stop_motors(200)
    # back up
    straight_drive_black(-40, False)
    straight_drive_distance(-40, 4, False)
    square_up_black(30, 30)
    square_up_white(-15, -15)
    square_up_black(10, 10)
    square_up_white(-5, -5)
    stop_motors(100)
    # turn left towards green ring
    ROBOT.run(gyro_turn, red=(-40, 40, 63),  green=(-40, 40, 66, False))
    stop_motors(200)
    # back up
    straight_drive_distance(-40, 3, False)
    stop_motors()
    # put arm into position to grab green ring
    servo.move(Arm.GREEN_RING_PICKUP, 1, 2)
    msleep(100)
    # move forwards to pick up green ring
    straight_drive_distance(40, 7.5, False)
    stop_motors(200)
    # grab the green ring
    servo.move(Claw.YELLOW_RING, 0)
    straight_drive_distance(-40, 2, False)
    stop_motors()
    # move the arm up
    servo.move(Arm.TALL_RING_DELIVERY, 1, 2)
    msleep(100)
    # back up
    straight_drive_distance(-40, 1.5, False)
    stop_motors(200)
    if left_green:
        # turn right
        gyro_turn(40, -40, 65, False)
        stop_motors(200)
        # square up on black
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)
        stop_motors(100)
        # move forwards
        straight_drive_distance(35, 2, False)
        ROBOT.run(straight_drive_distance, red=(70, 18.5, False), green=(70, 16, False))
        straight_drive_distance(35, 2, False)
        stop_motors(200)
        # turn right towards tower
        ROBOT.run(gyro_turn, red=(40, -40, 85, False), green=(40, -40, 91, False))
        stop_motors(200)
        # move forwards
        straight_drive_distance(40, 12, False)
        stop_motors()
        # open claw
        servo.move(Claw.OPEN, 1)
        rake_manager.position = RakePositions.MIDDLE_KEY
        # back up so we don't break
        straight_drive_distance(-20, 0.5, False)
        rake_manager.position = RakePositions.MIDDLE_KEY_PULL
        straight_drive_distance(-20, 4.9, False)
        rake_manager.position = RakePositions.REST
        straight_drive_distance(-40, 3, False)
        stop_motors(200)
        gyro_turn(40, -40, 90, False)
        stop_motors(200)
        straight_drive_distance(50, 12, False)
        straight_drive_black(40, False)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        ROBOT.run(gyro_turn, red=(40, -40, 77), green=(40, -40, 79, False))
        stop_motors(200)
        straight_drive_distance(-40, 3, False)
        stop_motors()
        servo.move(Arm.BLUE_RING_PICKUP, 1, 2)
        msleep(100)
        straight_drive_distance(40, 4, False)
        straight_drive_distance(30, 3.5, False)
        servo.move(Claw.YELLOW_RING, 0)
        servo.move(Arm.REST_POSITION, 1, 2)
        msleep(100)
        straight_drive_distance(-30, 5, False)
        stop_motors()
        servo.move(Arm.TALL_RING_DELIVERY, 1, 2)
        msleep(100)
        gyro_turn(-40, 40, 74, False)
        stop_motors(200)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)
        stop_motors(100)

        # move forwards
        straight_drive_distance(35, 2, False)
        straight_drive_distance(70, 14, False)
        straight_drive_distance(35, 2, False)
        stop_motors(200)
        # turn left towards tower
        ROBOT.run(gyro_turn, red=(-40, 40, 95, False), green=(-40, 40, 93, False))
        stop_motors(200)
        # move forwards
        straight_drive_distance(40, 12, False)
        stop_motors()
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-15, 0.1, False)
        rake_manager.position = RakePositions.HIGH_KEY + 220
        straight_drive_distance(-15, 1.5, False)
        rake_manager.position = RakePositions.HIGH_KEY_PULL
        ROBOT.run(straight_drive_distance, red=(-15, 4, False), green=(-15, 4.4, False))
        stop_motors(100)
        rake_manager.position = RakePositions.REST
        ROBOT.run(straight_drive_distance, red=(-50, 9.6), green=(-50, 9.2, False))
        stop_motors(300)
    else:
        # turn left
        gyro_turn(-40, 40, 120, False)
        stop_motors(200)
        # drive back past the black line
        straight_drive_distance(-40, 2, False)
        straight_drive_black(-70, False)
        straight_drive_distance(-40, 2, False)
        # square up on black
        square_up_black(30, 30)
        square_up_white(-20, -20)
        square_up_black(10, 10)
        square_up_white(-5, -5)
        stop_motors(100)
        # move forwards
        straight_drive_distance(35, 2, False)
        straight_drive_distance(70, 13.5, False)
        straight_drive_distance(35, 2, False)
        stop_motors(200)
        # turn left towards tower
        gyro_turn(-40, 40, 91, False)
        stop_motors(200)
        # move forwards
        straight_drive_distance(40, 12, False)
        stop_motors()
        # open claw
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-20, 0.1, False)
        rake_manager.position = RakePositions.HIGH_KEY
        straight_drive_distance(-20, 0.5, False)
        rake_manager.position = RakePositions.HIGH_KEY_PULL
        straight_drive_distance(-20, 3.9, False)
        rake_manager.position = RakePositions.REST
        straight_drive_distance(-40, 4.5, False)
        stop_motors(200)

        gyro_turn(-40, 40, 90, False)
        stop_motors(200)
        straight_drive_distance(40, 8, False)
        straight_drive_black(30, False)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        stop_motors(100)
        ROBOT.run(gyro_turn, red=(-40, 40, 60, False), green=(-40, 40, 62, False))
        stop_motors(200)
        straight_drive_distance(-30, 1, False)
        stop_motors(400)
        servo.move(Arm.BLUE_RING_PICKUP, 1, 2)
        msleep(200)
        straight_drive_distance(40, 4, False)
        straight_drive_distance(30, 3.5, False)
        servo.move(Claw.YELLOW_RING, 0)
        stop_motors(200)
        straight_drive_distance(-30, 2, False)
        straight_drive_distance(-60, 2.5, False)
        straight_drive_distance(-30, 2, False)
        stop_motors(200)
        servo.move(Arm.TALL_RING_DELIVERY, 1, 2)
        msleep(200)
        gyro_turn(40, -40, 67, False)
        stop_motors(200)
        square_up_black(30, 30)
        square_up_white(-15, -15)
        square_up_black(5, 5)
        square_up_white(-5, -5)

        # move forwards
        straight_drive_distance(35, 2, False)
        ROBOT.run(straight_drive_distance, red=(70, 16.3, False), green=(70, 16.3, False))
        straight_drive_distance(35, 2, False)
        stop_motors(200)
        # turn right towards tower
        ROBOT.run(gyro_turn, red=(40, -40, 89, False), green=(40, -40, 88, False))
        stop_motors(200)
        # move forwards
        straight_drive_distance(40, 13, False)
        stop_motors()
        # open claw
        rake_manager.position = RakePositions.MIDDLE_KEY + 100
        servo.move(Claw.OPEN, 1)
        # back up so we don't break
        straight_drive_distance(-15, 1.2, False)
        rake_manager.position = RakePositions.MIDDLE_KEY_PULL + 30
        straight_drive_distance(-15, 4.2, False)
        rake_manager.position = RakePositions.REST
        straight_drive_distance(-40, 8.6, False)
        stop_motors(200)


def get_bumps():
    data = query_create([Opcode.QUERY_LIST, 1, 7], 1)
    return data != b'\x00'


def get_encoder_values():
    left, right = encoders.values
    return -1 * left, -1 * right


def shutdown():
    rake_manager.position = RakePositions.END
    servo.move(Arm.REST_POSITION, 1)
    rake_manager.running = False
    disable_servos()
    print(str(round(time()-start_time, 2)) + " seconds elapsed total.")


def wait(duration):
    msleep(100)
    drive(0, 0, duration - 200)
    msleep(100)
    print('waiting')


def drive_until_bump(speed):
    straight_drive(speed, get_bumps, condition_is=False)
