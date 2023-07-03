#!/usr/local/bin/python3.10 -u
from typing import Optional
from kipr import *
from time import time
import os
from enum import IntEnum


class TowerColor(IntEnum):
    NOODLE = 0
    GREEN = 1
    BLUE = 2


# gameboard.conf
COLOR_PROXIMITY = 40

left_tower: Optional[int] = None
right_tower: Optional[int] = None

"""
HOW TO CALIBRATE CAMERA
1. Plug in camera
2. Home -> Settings -> Channels
3. Edit or Add a configuration
4. Select or Add a channel -> Configure
5. Point camera at target object and click on object onscreen
6. Adjust black and white boxes until area selected looks correct
7. Done -> Back -> Default -> Home

HOW TO USE CAMERA
1. Turn camera on (camera_open_black())
2. Take a picture (update_camera())
3. Get data on objects of target color in picture (eg get_object_area())
4. Run steps 2 and 3 in loop to look for the color (eg find_colors_manual())
"""


def init_camera():
    print("Running!")
    if camera_open_black() == 0:
        print("camera does not open")
        exit(0)
    else:
        print("camera open")
    if camera_update() == 0:
        print("no update")
    else:
        print("update")
    for i in range(30):  # update camera 5x over 5 seconds
        camera_update()
        msleep(100)


def color_define(tower_color):
    # Converts channel number to color
    return tower_color.name


def find_color(channel, min_area):
    print(channel)
    for i in range(5):  # update camera 5x
        camera_update()
        msleep(600)
    area = get_object_area(channel, 0)
    print(area)
    if area >= min_area:
        x_coord = get_object_center_x(channel, 0)
        y_coord = get_object_center_x(channel, 0)
        center = (x_coord, y_coord)
        print(center)
        return center
    else:
        print("no object of specified size and color found")


def color_proximity(color):
    # Tests to see if the center of the colored card is within a certain proximity to the red noodle
    if abs(get_object_center_x(color, 0) - get_object_center_x(TowerColor.NOODLE, 0)) < COLOR_PROXIMITY:
        return True
    if abs(get_object_center_x(color, 0) - get_object_center_x(TowerColor.NOODLE, 1)) < COLOR_PROXIMITY:
        return True
    return False


def get_tower_color(left_bound, right_bound, min_area=40):
    # Determines what color block is below the red noodle
    camera_update()
    # print("noodle area:", get_object_area(NOODLE, 0))
    if get_object_count(TowerColor.NOODLE) > 0 and get_object_area(TowerColor.NOODLE, 0) > 30:
        for color in [TowerColor.GREEN, TowerColor.BLUE]:
            # print(color_define(color), "area:", get_object_area(color, 0))
            # print("get obj center x:", color_define(color), get_object_center_x(color, 0))
            if get_object_area(color, 0) > min_area and color_proximity(color):
                # print("see", color_define(color), "outside of range")
                if left_bound < get_object_center_x(color, 0) < right_bound:
                    # print("color found:", color_define(color))
                    return color
            else:
                # print("do not see", color_define(color))
                pass
    else:
        print("do not see noodle")


def card_scan():
    global left_tower
    global right_tower
    temp = get_tower_color(0, 159)
    if temp is None:
        print("UH OH - MISSING LEFT CARD")
    else:
        left_tower = temp
        if left_tower == TowerColor.BLUE:
            right_tower = TowerColor.GREEN
        else:
            left_tower = TowerColor.GREEN
            right_tower = TowerColor.BLUE
        # print("TOWER COLORS")
        print("LEFT TOWER:", color_define(left_tower))
        # print("right tower:", color_define(right_tower))


def scan_continuously():
    scan_end = 0
    while not push_button():
        if time() - scan_end > 1:
            card_scan()
            scan_end = time()
    print("FINAL TOWER CARD COLORS")
    print("LEFT TOWER:", color_define(left_tower))
    # print("right tower:", color_define(right_tower))


def load_config():
    set_camera_config_base_path(os.path.dirname(__file__))
    camera_load_config("gameboard")


def is_left_green():
    # print(left_tower)
    return left_tower == TowerColor.GREEN


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     load_config()
#     init_camera()
#     wait_4_light(0, function=card_scan, function_every=1)

