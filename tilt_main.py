from microbit import *

my_level = 0
position_x = 2
position_y = 2
cycle = 0


def play_intro():
    display.clear()
    frame1 = Image("00000:"
                   "00000:"
                   "00000:"
                   "00000:"
                   "00000:")
    frame2 = Image("00000:"
                   "00000:"
                   "00500:"
                   "00000:"
                   "00000:")
    frame3 = Image("00000:"
                   "00900:"
                   "09090:"
                   "00900:"
                   "00000:")
    frame4 = Image("00900:"
                   "09090:"
                   "90309:"
                   "09090:"
                   "00900:")
    frame5 = Image("09090:"
                   "90009:"
                   "00500:"
                   "90009:"
                   "09090:")
    frame6 = Image("90009:"
                   "00000:"
                   "00900:"
                   "00000:"
                   "90009:")
    frame7 = Image("00000:"
                   "00000:"
                   "00900:"
                   "00000:"
                   "00000:")
    all_frames = [frame1, frame2, frame3, frame4, frame5, frame6, frame7]
    display.show(all_frames, delay=200)


level_01 = Image("50000:"
                 "33303:"
                 "30000:"
                 "30333:"
                 "30103:")
level_02 = Image("10000:"
                 "33303:"
                 "00000:"
                 "03333:"
                 "00005:")
level_03 = Image("50000:"
                 "33300:"
                 "30003:"
                 "00333:"
                 "00001:")
level_04 = Image("33330:"
                 "33000:"
                 "50001:"
                 "33000:"
                 "33330:")
level_05 = Image("00005:"
                 "33033:"
                 "30003:"
                 "00000:"
                 "00100:")
level_06 = Image("10033:"
                 "30003:"
                 "33300:"
                 "33330:"
                 "50000:")
level_07 = Image("00010:"
                 "00000:"
                 "00333:"
                 "03350:"
                 "00000:")
level_08 = Image("30000:"
                 "00330:"
                 "13500:"
                 "00330:"
                 "30033:")
level_09 = Image("00000:"
                 "03303:"
                 "03103:"
                 "03335:"
                 "00000:")

levels = [level_01, level_02, level_03, level_04, level_05, level_06, level_07, level_08, level_09]


def play_level_intro():
    global levels, my_level, position_x, position_y
    display.clear()
    display.show(str(my_level + 1))
    sleep(1000)
    display.clear()
    display.show(levels[my_level])
    position_x, position_y = find_start()


def find_treasure():
    global levels, my_level
    for x in range(5):
        for y in range(5):
            if display.get_pixel(x, y) == 5:
                return x, y
    return 0, 0


def find_start():
    global levels, my_level
    for x in range(5):
        for y in range(5):
            if display.get_pixel(x, y) == 1:
                return x, y
    return 2, 2


def play_victory():
    global levels, my_level
    display.clear()
    display.show(levels[my_level])
    sleep(400)
    display.clear()
    sleep(400)
    display.clear()
    display.show(levels[my_level])
    sleep(400)
    display.clear()
    sleep(400)
    if my_level < len(levels) - 1:
        my_level += 1
        play_level_intro()
    else:
        # you win
        my_level = 0
        display.show("you win!")
        sleep(200)
        play_intro()


def run():
    global position_x, position_y, levels, my_level, cycle

    cycle += 1

    display.clear()
    display.show(levels[my_level])

    treasure_x, treasure_y = find_treasure()
    start_x, start_y = find_start()
    display.set_pixel(start_x, start_y, 0)

    if cycle % 3 == 0:
        display.set_pixel(treasure_x, treasure_y, 1)

    roll = accelerometer.get_x()
    pitch = accelerometer.get_y()

    last_x = position_x
    last_y = position_y

    if roll > 20:
        if position_x < 4:
            position_x += 1
    elif roll < -20:
        if position_x > 0:
            position_x -= 1

    if pitch > 20:
        if position_y < 4:
            position_y += 1
    elif pitch < -20:
        if position_y > 0:
            position_y -= 1

    if display.get_pixel(position_x, position_y) == 3:
        # hit a wall, bump back
        position_x = last_x
        position_y = last_y

    display.set_pixel(position_x, position_y, 9)

    if position_x == treasure_x and position_y == treasure_y:
        play_victory()
    else:
        sleep(100)


play_intro()
play_level_intro()

# main loop, run forever
while 1:
    run()
