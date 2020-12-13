import sys
import math
import numpy as np


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse(line):
    return line[0], int(line[1:])


def parse_file(filename):
    return [parse(line) for line in stripped_lines(filename)]


def rotate(action, amount, vector):
    rads = amount * math.pi / 180.0
    if action == 'R':
        rads = -rads
    rot = np.array([
        [math.cos(rads), -math.sin(rads)],
        [math.sin(rads), math.cos(rads)],
    ])
    return np.dot(rot, vector)

def simulate1(values):
    facing = np.array([1, 0])
    xpos = 0
    ypos = 0
    for action, amount in values:
        if action == 'N':
            ypos += amount
        elif action == 'S':
            ypos -= amount
        elif action == 'E':
            xpos += amount
        elif action == 'W':
            xpos -= amount
        elif action == 'L' or action == 'R':
            facing = rotate(action, amount, facing)
        elif action == 'F':
            xpos += amount * facing[0]
            ypos += amount * facing[1]
    return xpos, ypos


def simulate2(values):
    boat_x = 0
    boat_y = 0
    way_x = 10
    way_y = 1
    for action, amount in values:
        if action == 'N':
            way_y += amount
        elif action == 'S':
            way_y -= amount
        elif action == 'E':
            way_x += amount
        elif action == 'W':
            way_x -= amount
        elif action == 'L' or action == 'R':
            way = rotate(action, amount, np.array([way_x, way_y]))
            way_x = way[0]
            way_y = way[1]
        elif action == 'F':
            boat_x += amount * way_x
            boat_y += amount * way_y
    return boat_x, boat_y


def main(args):
    inputs = parse_file(args[1])
    xpos, ypos = simulate1(inputs)
    p1_ans = int(round(abs(xpos) + abs(ypos)))
    print(f'part one: {p1_ans}')
    xpos, ypos = simulate2(inputs)
    p2_ans = int(round(abs(xpos) + abs(ypos)))
    print(f'part two: {p2_ans}')
    # part one: 1631
    # part two: 58606


if __name__ == '__main__':
    main(sys.argv)