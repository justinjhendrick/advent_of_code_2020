import sys
from collections import defaultdict


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_file(filename):
    z = 0
    w = 0

    y = 0
    conway = defaultdict(int)
    for line in stripped_lines(filename):
        x = 0
        for char in line:
            conway[(x, y, z, w)] = (char == '#')
            x += 1
        y -= 1
    return conway


def nearby_or_one(lo, hi, yield_all):
    if not yield_all:
        yield lo
    else:
        for v in range(lo, hi):
            yield v


def count_neighbors(conway, coords):
    ndim = len(coords)
    my_x = coords[0]
    my_y = coords[1]
    my_z = coords[2]
    my_w = coords[3] if ndim == 4 else 0
    result = 0
    for x in range(my_x - 1, my_x + 2):
        for y in range(my_y - 1, my_y + 2):
            for z in range(my_z - 1, my_z + 2):
                for w in nearby_or_one(my_w - 1, my_w + 2, ndim == 4):
                    if x == my_x and y == my_y and z == my_z and w == my_w:
                        continue
                    result += conway[(x, y, z, w)]
    return result


def bounds(conway):
    xs = []
    ys = []
    zs = []
    ws = []
    for coord, is_active in conway.items():
        if is_active:
            x, y, z, w = coord
            xs.append(x)
            ys.append(y)
            zs.append(z)
            ws.append(w)
    return [
        (min(xs) - 1, max(xs) + 2),
        (min(ys) - 1, max(ys) + 2),
        (min(zs) - 1, max(zs) + 2),
        (min(ws) - 1, max(ws) + 2),
    ]


def run(conway, ndim, ncycles=6):
    new_conway = defaultdict(bool)
    for i in range(ncycles):
        bds = bounds(conway)
        x_lo, x_hi = bds[0]
        y_lo, y_hi = bds[1]
        z_lo, z_hi = bds[2]
        w_lo, w_hi = bds[3] if ndim == 4 else (0, 0)
        for x in range(x_lo, x_hi):
            for y in range(y_lo, y_hi):
                for z in range(z_lo, z_hi):
                    for w in nearby_or_one(w_lo, w_hi, ndim == 4):
                        coords = x, y, z, w
                        is_active = conway[coords]
                        num_neighbors = count_neighbors(conway, coords)
                        if is_active and (num_neighbors == 2 or num_neighbors == 3):
                            new_conway[coords] = True
                        elif (not is_active) and num_neighbors == 3:
                            new_conway[coords] = True
        conway = new_conway
        new_conway = defaultdict(bool)
    return sum(v for v in conway.values())


def main(args):
    inputs = parse_file(args[1])
    p1_ans = run(inputs, 3)
    print(f'part one: {p1_ans}')
    p2_ans = run(inputs, 4)
    print(f'part two: {p2_ans}')
    # part one: 333
    # part two: 2676


if __name__ == '__main__':
    main(sys.argv)
