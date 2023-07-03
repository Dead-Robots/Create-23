from kipr import set_servo_position, get_servo_position, disable_servo, enable_servo
from time import sleep


def msleep(milliseconds):
    sleep(milliseconds/1000)


def move(new_position, step_time=2, increment=1):
    servo = new_position.port
    temp = get_servo_position(servo)

    if temp < new_position:
        while temp < new_position:
            set_servo_position(servo, temp)
            temp += increment
            msleep(step_time)
    else:
        while temp > new_position:
            set_servo_position(servo, temp)
            temp -= increment
            msleep(step_time)
