import sys
from collections import defaultdict
import pyparsing as pp


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def make_grammar():
    color = pp.Combine(pp.Word(pp.alphas) + pp.Word(pp.alphas), adjacent=False, joinString=' ') 
    bag = color + pp.oneOf(['bag', 'bags'])
    bags = pp.Group(
        (pp.Word(pp.nums) + bag) |
        ('no other bags')
    )
    return bag + 'contain' + pp.delimitedList(bags) + '.'


def lex(filename):
    grammar = make_grammar()
    return [grammar.parseString(line) for line in stripped_lines(filename)]


def parse(filename):
    all_tokens = lex(filename)
    contained = defaultdict(list)
    contains = defaultdict(list)
    for tokens in all_tokens:
        outer_color = tokens[0]
        # 'bags' == tokens[1]
        # 'contain' == tokens[2]
        # '.' == tokens[-1]
        inner_colors = []
        for bags in tokens[3:-1]:
            if bags[0] == 'no other bags':
                continue
            count = bags[0]
            inner_color = bags[1]
            # 'bag(s)' = bags[2]
            contained[inner_color].append(outer_color)
            contains[outer_color].append((inner_color, int(count)))
    return (contained, contains)


def find_reachable(start, edges):
    # depth first search
    result = set()
    for e in edges[start]:
        result.add(e)
        result = set.union(result, find_reachable(e, edges))
    return result


def count_total_bags_inside(start, edges):
    # depth first search
    result = 0
    for e, count in edges[start]:
        result += count + count * count_total_bags_inside(e, edges)
    return result


def main(args):
    contained, contains = parse(args[1])
    p1_ans = len(find_reachable('shiny gold', contained))
    print(f'part one: {p1_ans}')
    p2_ans = count_total_bags_inside('shiny gold', contains)
    print(f'part two: {p2_ans}')
    # part one: 261
    # part two: 3765


if __name__ == '__main__':
    main(sys.argv)