import sys
from collections import defaultdict
import re


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_file(filename):
    lines = list(stripped_lines(filename))
    state = 0
    rules = defaultdict(list)
    messages = []
    for line in lines:
        if line == '':
            state += 1
        elif state == 0:
            kv = line.split(':')
            key = int(kv[0])
            values = kv[1]
            if '"' in values:
                start = values.find('"')
                end = values.rfind('"')
                rules[key].append(values[start + 1:end])
            else:
                for group in values.split('|'):
                    refs = [int(ref) for ref in group.split(' ') if ref != '']
                    rules[key].append(refs)
        elif state == 1:
            messages.append(line)
    return rules, messages


def build_regex(rules, key, part_num):
    groups = rules[key]
    if isinstance(groups[0], str):
        return groups[0]

    if part_num == 2 and (key == 8 or key == 11):
        r42 = build_regex(rules, 42, part_num)
        r31 = build_regex(rules, 31, part_num)
        if key == 8:
            return '(' + r42 + '+)'
        elif key == 11:
            return '(' + '|'.join([r42 + '{' + str(i) + '}' + r31 + '{' + str(i) + '}' for i in range(1, 5)]) + ')'

    result = []
    for group in groups:
        group_regex = ''.join((build_regex(rules, key, part_num) for key in group))
        result.append(group_regex)
    pre = '^' if key == 0 else '('
    post = '$' if key == 0 else ')'
    return pre + '|'.join(result) + post


def run(inputs, part_num):
    rules, messages = inputs
    rx_str = build_regex(rules, 0, part_num)
    rx = re.compile(rx_str)
    num_valid = 0
    for m in messages:
        matches = rx.match(m)
        if matches is not None:
            num_valid += 1
    return num_valid


def main(args):
    inputs = parse_file(args[1])
    p1_ans = run(inputs, 1)
    print(f'part one: {p1_ans}')
    p2_ans = run(inputs, 2)
    print(f'part two: {p2_ans}')
    # part one: 132
    # part two: 306


if __name__ == '__main__':
    main(sys.argv)
