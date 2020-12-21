import sys
from collections import defaultdict
import re
import pyparsing as pp
from functools import reduce
import operator


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
        if key == 8:
            return '(' + build_regex(rules, 42, part_num) + '+)'
        elif key == 11:
            return '(?P<left>' + build_regex(rules, 42, part_num) + '+)' + \
                   '(?P<right>' + build_regex(rules, 31, part_num) + '+)'

    result = []
    for group in groups:
        group_regex = ''.join((build_regex(rules, key, part_num) for key in group))
        result.append(group_regex)
    pre = '^' if key == 0 else '('
    post = '$' if key == 0 else ')'
    return pre + '|'.join(result) + post


# def build_grammar(rules, key):
#    groups = rules[key]
#    if isinstance(groups[0], str):
#        return pp.Literal(groups[0])
#    # elif key == 8:
#    #    result = pp.OneOrMore(build_grammar(rules, 42))
#    #    #result.setName('8')
#    #    return result
#    # elif key == 11:
#    #    result = pp.OneOrMore(build_grammar(rules, 42)) + pp.OneOrMore(build_grammar(rules, 31))
#    #    #result.setName('11')
#    #    return result
#    else:
#        options = []
#        for group in groups:
#            group_regex = reduce(lambda x, y: x + y,
#                                 (build_grammar(rules, key) for key in group))
#            options.append(group_regex)
#        return reduce(lambda x, y: x | y, options)


def p1(inputs):
    rules, messages = inputs
    rx_str = build_regex(rules, 0, 1)
    rx = re.compile(rx_str)
    num_valid = 0
    for m in messages:
        matches = rx.match(m)
        if matches is not None:
            num_valid += 1
    return num_valid


def p2(inputs):
    rules, messages = inputs
    rx_str = build_regex(rules, 0, 2)
    rx = re.compile(rx_str)
    num_valid = 0
    for m in messages:
        matches = rx.match(m)
        if matches is not None:
            num_left_matches = len(re.findall(build_regex(rules, 42, 2), matches.group('left')))
            num_right_matches = len(re.findall(build_regex(rules, 31, 2), matches.group('right')))
            print(m, num_left_matches, num_right_matches)
            if num_left_matches == num_right_matches:
                num_valid += 1
    return num_valid


# def grammar_match(g, m):
#    try:
#        result = g.parseString(m)
#        #eight = result.getName('8')
#        #eleven = result.getName('11')
#        return True
#    except pp.ParseException:
#        return False
#
#
# def p2(inputs):
#    rules, messages = inputs
#    grammar = build_grammar(rules, 0)
#    print(grammar)
#    num_valid = 0
#    for m in messages:
#        match = grammar_match(grammar, m)
#        if match:
#            num_valid += 1
#    return num_valid


def main(args):
    inputs = parse_file(args[1])
    p1_ans = p1(inputs)
    print(f'part one: {p1_ans}')
    p2_ans = p2(inputs)
    print(f'part two: {p2_ans}')


if __name__ == '__main__':
    main(sys.argv)
