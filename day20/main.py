import sys
from functools import reduce
import operator


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_tile(lines):
    identifier = int(lines[0].split(' ')[1][:-1])
    image = lines[1:]
    return identifier, image


def parse_file(filename):
    result = []
    tile_lines = []
    for line in stripped_lines(filename):
        if line == '':
            result.append(parse_tile(tile_lines))
            tile_lines = []
        else:
            tile_lines.append(line)
    result.append(parse_tile(tile_lines))
    return result


def get_edges(image):
    result = []
    left = []
    right = []
    for i in range(len(image)):
        row = image[i]
        if i == 0 or i == len(image) - 1:
            result.append(row)
        for j in range(len(image)):
            if j == 0:
                left.append(row[j])
            elif j == len(row) - 1:
                right.append(row[j])
    result.append(''.join(left))
    result.append(''.join(right))
    return result


def add_flips(edges):
    flips = []
    for e in edges:
        flips.append(e[::-1])
    return edges + flips


def match(tile1, tile2):
    _, image1 = tile1
    _, image2 = tile2
    count = 0
    for edge1 in add_flips(get_edges(image1)):
        for edge2 in add_flips(get_edges(image2)):
            if edge1 == edge2:
                count += 1
    return count
    

def p1(inputs):
    corners = []
    for i in range(len(inputs)):
        num_matching_edges = 0
        for j in range(len(inputs)):
            if i == j:
                continue
            if match(inputs[i], inputs[j]):
                num_matching_edges += 1
        if num_matching_edges == 2:
            corners.append(inputs[i][0])
    assert len(corners) == 4
    return reduce(operator.mul, corners, 1)


def p2(inputs):
    pass


def main(args):
    inputs = parse_file(args[1])
    p1_ans = p1(inputs)
    print(f'part one: {p1_ans}')
    p2_ans = p2(inputs)
    print(f'part two: {p2_ans}')


if __name__ == '__main__':
    main(sys.argv)
