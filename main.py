from math import pi

import curses
import math
import os

if os.path.exists("log"):
    os.remove("log")

screen = curses.initscr()
screen.nodelay(1)
curses.cbreak()
curses.noecho()

width, height = 16, 16
screen_height, screen_width = screen.getmaxyx()
screen_height -= 1
player_x, player_y = 7.3, 10
player_a = pi / 2
view_angle = pi / 4
MAX_DIST = 16

grid_map = [
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
]

def log(text):
    text = str(text)
    with open("log", "a") as fout:
        fout.write(text + "\n")

def standardize(angle: float) -> float:
    '''
    convert any angle outside of range [0, 2π] to this range
    '''
    while not (0 <= angle and angle <= 2 * pi):
        angle = angle + pi * 2 if angle < 0 else angle - pi * 2

    return angle

def dist_to_wall(x: float, y: float, angle: float) -> float:
    '''
    return the distance to closest wall
    '''
    angle = standardize(angle)
    dx, dy = math.cos(angle), math.sin(angle)
    distance = 0.1
    hit_wall = False

    while not hit_wall:
        distance += 0.1

        _x = int( player_x + dx * distance )
        _y = int( player_y + dy * distance )

        if _x < 0 or _x >= width or _y < 0 or _y >= height:
            distance = MAX_DIST
            hit_wall = True
        else:
            if grid_map[_y][_x] == '#':
                hit_wall = True

    return distance

def get_floor(fl: int):
    ratio = fl / screen_height

    if ratio < 0.6:
        return ' '
    elif ratio < 0.7:
        return '.'
    elif ratio < 0.8:
        return '-'
    elif ratio < 0.9:
        return 'x'
    else:
        return '#'

def get_wall(ratio: float):
    if ratio < 0.1:
        return ' '
    elif ratio < 0.25:
        return '\u2591'
    elif ratio < 0.5:
        return '\u2592'
    elif ratio < 0.75:
        return '\u2593'
    else:
        return '\u2588'

def in_map(x: int, y: int) -> bool:
    return 0 <= x and x < width and 0 <= y and y < height

if __name__ == "__main__":
    while True:
        ch_in = screen.getch()
        if ch_in == ord("l"):
            player_a += 0.05

        elif ch_in == ord("j"):
            player_a -= 0.05

        elif ch_in == ord("i"):
            player_x += 0.1 * math.cos(player_a)
            player_y += 0.1 * math.sin(player_a)

            if not in_map(int(player_x), int(player_y)) or grid_map[int(player_y)][int(player_x)] == "#":
                player_x -= 0.1 * math.cos(player_a)
                player_y -= 0.1 * math.sin(player_a)

        elif ch_in == ord("k"):
            player_x -= 0.1 * math.cos(player_a)
            player_y -= 0.1 * math.sin(player_a)

            if not in_map(int(player_x), int(player_y)) or grid_map[int(player_y)][int(player_x)] == "#":
                player_x += 0.1 * math.cos(player_a)
                player_y += 0.1 * math.sin(player_a)

        elif ch_in == ord("q"):
            break

        for i in range(screen_width):
            angle = ( player_a - view_angle / 2 ) + i / screen_width * view_angle

            dist = dist_to_wall(player_x, player_y, angle)
            ratio = (1 - dist / MAX_DIST)
            wall_type = get_wall(ratio)

            n_floor = int(screen_height // 2 * ( 1 - ratio ))
            n_ceiling = n_floor
            n_wall = screen_height - n_floor * 2

            for j in range(n_ceiling):
                screen.addstr(j, i, " ")

            for j in range(n_wall):
                screen.addstr(n_ceiling + j, i, wall_type)

            for j in range(n_floor):
                screen.addstr(n_ceiling + n_wall + j, i, get_floor(n_ceiling + n_wall + j))

        screen.refresh()

    curses.endwin()
