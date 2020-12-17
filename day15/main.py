import sys
from collections import defaultdict


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_file(filename):
    line = next(stripped_lines(filename))
    return [int(v) for v in line.split(',')]


def run(inputs, end):
    memory = {}
    prev = None
    for i in range(end):
        if i < len(inputs):
            curr = inputs[i]
        else:
            if prev in memory:
                curr = (i - 1) - memory[prev]
            else:
                curr = 0
        memory[prev] = i - 1
        prev = curr
    return curr


def p1(inputs):
    return run(inputs, 2020)


def p2(inputs):
    return run(inputs, 30000000)


def test():
    assert p1([0, 3, 6]) == 436
    assert p1([1, 3, 2]) == 1
    assert p1([2, 1, 3]) == 10
    assert p1([1, 2, 3]) == 27
    assert p1([2, 3, 1]) == 78
    assert p1([3, 2, 1]) == 438
    assert p1([3, 1, 2]) == 1836


def main(args):
    test()
    inputs = parse_file(args[1])
    p1_ans = p1(inputs)
    print(f'part one: {p1_ans}')
    p2_ans = p2(inputs)
    print(f'part two: {p2_ans}')
    # part one: 1009
    # part two: 62714


if __name__ == '__main__':
    main(sys.argv)
