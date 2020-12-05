import sys
from functools import reduce


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def partition_helper(chars, down_char, up_char, lower_bound, upper_bound):
    for char in chars:
        half = (upper_bound - lower_bound) / 2
        if char == down_char:
            upper_bound -= half
        elif char == up_char:
            lower_bound += half
        else:
            raise Exception("UNEXPECTED CHAR")
    assert lower_bound + 1 == upper_bound
    return lower_bound


def parse_partition_code(line):
    row = partition_helper(line[0:7], 'F', 'B', 0, 128)
    col = partition_helper(line[7:], 'L', 'R', 0, 8)
    return row, col


def parse(lines):
    ids = []
    for line in lines:
        row, col = parse_partition_code(line)
        ids.append(row * 8 + col)
    return ids


def highest_seat_id(ids):
    return reduce(max, ids, 0)


def my_seat(ids):
    ids.sort()
    for i in range(1, len(ids)):
        prev = ids[i - 1]
        curr = ids[i]
        if prev + 1 != curr:
            return prev + 1
    return None


def main(args):
    ids = parse(stripped_lines(args[1]))
    p1_ans = highest_seat_id(ids)
    print(f'part one: {p1_ans}')
    p2_ans = my_seat(ids)
    print(f'part two: {p2_ans}')
    # part one: 861.0
    # part two: 633.0


if __name__ == '__main__':
    main(sys.argv)