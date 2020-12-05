import sys


def parse(args):
    with open(args[1], mode='r') as f:
        return [line.strip() for line in f.readlines()]


def split(s, sep):
    pieces = s.split(sep)
    return pieces[0], sep.join(pieces[1:])


def parse_line(line):
    num_str, rest = split(line, '-')
    n1 = int(num_str)
    num_str, rest = split(rest, ' ')
    n2 = int(num_str)
    check_char, password = split(rest, ': ')
    return n1, n2, check_char, password


def count_valid_passwords(lines):
    num_valid = 0
    for line in lines:
        lower_bd, upper_bd, check_char, password = parse_line(line)
        count = sum([char == check_char for char in password])
        num_valid += (lower_bd <= count and count <= upper_bd)
    return num_valid

def position_valid_passwords(lines):
    num_valid = 0
    for line in lines:
        idx1, idx2, check_char, password = parse_line(line)
        idxs = [idx1, idx2]
        num_matches = sum([password[i - 1] == check_char for i in idxs])
        num_valid += (num_matches == 1)
    return num_valid

        
def main(args):
    lines = parse(args)
    p1_ans = count_valid_passwords(lines)
    print(f'part one: {p1_ans}')
    p2_ans = position_valid_passwords(lines)
    print(f'part two: {p2_ans}')
    # part one: 546
    # part two: 275


if __name__ == '__main__':
    main(sys.argv)