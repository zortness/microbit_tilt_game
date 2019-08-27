from microbit import *

my_level = 0
position_x = 2
position_y = 2
cycle = 0

intro_01 = Image("00000:"
                 "00000:"
                 "00000:"
                 "00000:"
                 "00000:")
intro_02 = Image("00000:"
                 "00000:"
                 "00500:"
                 "00000:"
                 "00000:")
intro_03 = Image("00000:"
                 "00900:"
                 "09090:"
                 "00900:"
                 "00000:")
intro_04 = Image("00900:"
                 "09090:"
                 "90309:"
                 "09090:"
                 "00900:")
intro_05 = Image("09090:"
                 "90009:"
                 "00500:"
                 "90009:"
                 "09090:")
intro_06 = Image("90009:"
                 "00000:"
                 "00900:"
                 "00000:"
                 "90009:")
intro_07 = Image("00000:"
                 "00000:"
                 "00900:"
                 "00000:"
                 "00000:")

intro_frames = [intro_01, intro_02, intro_03, intro_04, intro_05, intro_06, intro_07]


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
                 "33334:")
level_05 = Image("40005:"
                 "33033:"
                 "30003:"
                 "00000:"
                 "00100:")
level_06 = Image("10033:"
                 "30003:"
                 "33400:"
                 "33330:"
                 "50000:")
level_07 = Image("00010:"
                 "00000:"
                 "00333:"
                 "03354:"
                 "00000:")
level_08 = Image("40000:"
                 "00330:"
                 "13500:"
                 "00330:"
                 "30033:")
level_09 = Image("00004:"
                 "03303:"
                 "03103:"
                 "03335:"
                 "00000:")

levels = [level_01, level_02, level_03, level_04, level_05, level_06, level_07, level_08, level_09]


def play_intro():
    global intro_frames
    display.clear()
    display.show(intro_frames, delay=200)


def play_level_intro():
    global levels, my_level, position_x, position_y
    display.clear()
    display.show(str(my_level + 1))
    sleep(1000)
    display.clear()
    display.show(levels[my_level])
    position_x, position_y = find_start()


def find_treasure():
    for x in range(5):
        for y in range(5):
            if display.get_pixel(x, y) == 5:
                return x, y
    return 0, 0


def find_start():
    for x in range(5):
        for y in range(5):
            if display.get_pixel(x, y) == 1:
                return x, y
    return 2, 2


def find_trap():
    for x in range(5):
        for y in range(5):
            if display.get_pixel(x, y) == 4:
                return x, y
    # if there's no trap, set the position to off the map
    return -1, -1


def play_defeat():
    global my_level, intro_frames
    my_level = 0
    display.clear()
    display.show(intro_frames[::-1], delay=200)
    display.show("game over")
    display.clear()
    sleep(250)
    play_intro()
    play_level_intro()


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
        # go to next level
        my_level += 1
        play_level_intro()
    else:
        # you win
        my_level = 0
        display.show("you win")
        sleep(200)
        play_intro()


def test_collision(x, y):
    if x < 0 or x > 4 or y < 0 or y > 4:
        return True
    if display.get_pixel(x, y) == 3:
        return True
    return False


def run():
    global position_x, position_y, levels, my_level, cycle
    cycle += 1

    display.clear()
    display.show(levels[my_level])

    treasure_x, treasure_y = find_treasure()
    trap_x, trap_y = find_trap()
    start_x, start_y = find_start()
    # turn off "start" pixel
    display.set_pixel(start_x, start_y, 0)

    if cycle % 3 == 0:
        display.set_pixel(treasure_x, treasure_y, 1)
    if cycle % 10 == 0 and trap_x >= 0 and trap_y >= 0:
        display.set_pixel(trap_x, trap_y, 0)

    roll = accelerometer.get_x()
    pitch = accelerometer.get_y()

    if roll > 20:
        if not test_collision(position_x + 1, position_y):
            position_x += 1
    elif roll < -20:
        if not test_collision(position_x - 1, position_y):
            position_x -= 1

    if pitch > 20:
        if not test_collision(position_x, position_y + 1):
            position_y += 1
    elif pitch < -20:
        if not test_collision(position_x, position_y - 1):
            position_y -= 1

    # draw player pixel
    display.set_pixel(position_x, position_y, 9)

    if position_x == treasure_x and position_y == treasure_y:
        play_victory()
    elif position_x == trap_x and position_y == trap_y:
        play_defeat()
    else:
        sleep(100)


play_intro()
play_level_intro()

# main loop, run forever
while 1:
    run()
