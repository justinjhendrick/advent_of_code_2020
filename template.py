import sys


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse(line):
    pass


def parse_file(filename):
    return [parse(line) for line in stripped_lines(filename)]


def p1(values):
    pass


def p2(values):
    pass


def main(args):
    inputs = parse_file(args[1])
    p1_ans = p1(inputs)
    print(f'part one: {p1_ans}')
    p2_ans = p2(inputs)
    print(f'part two: {p2_ans}')


if __name__ == '__main__':
    main(sys.argv)