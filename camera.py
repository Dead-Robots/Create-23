from typing import Optional
from kipr import camera_open_black, camera_update, msleep, get_object_area, get_object_center_x, get_object_count, \
    push_button

# gameboard.conf
NOODLE = 0
GREEN = 1
BLUE = 2

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
    for i in range(5):  # update camera 5x over 5 seconds
        camera_update()
        msleep(100)


def color_define(channel):
    # Converts channel number to color
    if channel == NOODLE:
        return "NOODLE"
    elif channel == GREEN:
        return "GREEN"
    elif channel == BLUE:
        return "BLUE"


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
    if abs(get_object_center_x(color, 0) - get_object_center_x(NOODLE, 0)) < COLOR_PROXIMITY:
        return True
    if abs(get_object_center_x(color, 0) - get_object_center_x(NOODLE, 1)) < COLOR_PROXIMITY:
        return True
    return False


def get_tower_color(left_bound, right_bound, min_area=40):
    # determines what color block is below the red noodle
    for i in range(10):
        camera_update()
        msleep(100)
    # print("noodle area:", get_object_area(NOODLE, 0))
    if get_object_count(NOODLE) > 0 and get_object_area(NOODLE, 0) > 30:
        for color in [GREEN, BLUE]:
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
    left_tower = get_tower_color(0, 159)
    if left_tower is None:
        print("UH OH - MISSING LEFT CARD")
    else:
        if left_tower == BLUE:
            right_tower = GREEN
        else:
            right_tower = BLUE
        print("TOWER COLORS")
        print("left tower:", color_define(left_tower))
        print("right tower:", color_define(right_tower))


def scan_continuously():
    while not push_button():
        card_scan()
        msleep(1000)
    print("FINAL TOWER CARD COLORS")
    print("left tower:", color_define(left_tower))
    print("right tower:", color_define(right_tower))
