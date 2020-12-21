import sys
import pyparsing as pp


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def make_grammer(part_num):
    if part_num == 1:
        grammar = pp.infixNotation(pp.Word(pp.nums), [
            (pp.oneOf(['+', '*']), 2, pp.opAssoc.LEFT),
        ])
    elif part_num == 2:
        grammar = pp.infixNotation(pp.Word(pp.nums), [
            (pp.Literal('+'), 2, pp.opAssoc.LEFT),
            (pp.Literal('*'), 2, pp.opAssoc.LEFT),
        ])
    return grammar


def parse(line, part_num):
    grammar = make_grammer(part_num)
    result = []
    for t in grammar.parseString(line).asList()[0]:
        result.append(t)
    return result


def parse_file(filename):
    lines = [line for line in stripped_lines(filename)]
    input1 = [parse(line, 1) for line in lines]
    input2 = [parse(line, 2) for line in lines]
    return input1, input2


def evaluate(tokens):
    if len(tokens) == 0:
        return 0

    def eval_one(t):
        return evaluate(t) if isinstance(t, list) else int(t)
    token = tokens[0]
    result = eval_one(token)
    op = None
    for token in tokens[1:]:
        if token == '*' or token == '+':
            op = token
        elif op == '+':
            result += eval_one(token)
        elif op == '*':
            result *= eval_one(token)
    return result


def run(inputs):
    return sum(evaluate(line) for line in inputs)


def test():
    assert evaluate(parse('2 * 3 + (4 * 5)', 1)) == 26
    assert evaluate(parse('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1)) == 437
    assert evaluate(
        parse('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 1)) == 12240
    assert evaluate(
        parse('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 1)) == 13632

    assert evaluate(parse('2 * 3 + (4 * 5)', 2)) == 46
    assert evaluate(parse('5 + (8 * 3 + 9 + 3 * 4 * 3)', 2)) == 1445
    assert evaluate(
        parse('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 2)) == 669060
    assert evaluate(
        parse('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 2)) == 23340


def main(args):
    test()
    input1, input2 = parse_file(args[1])
    p1_ans = run(input1)
    print(f'part one: {p1_ans}')
    p2_ans = run(input2)
    print(f'part two: {p2_ans}')
    # part one: 4297397455886
    # part two: 93000656194428


if __name__ == '__main__':
    main(sys.argv)
