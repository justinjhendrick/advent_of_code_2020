import sys


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_multiline(args, aggregate_function):
    result = []
    responses = []
    for line in stripped_lines(args[1]):
        if line == '':
            result.append(aggregate_function(responses))
            responses = []
        else:
            response = set()
            for char in line:
                response.add(char)
            responses.append(response)
    if len(response) != 0:
        result.append(aggregate_function(responses))

    return result


def main(args):
    p1_responses = parse_multiline(args, lambda x: set.union(*x))
    p1_ans = sum([len(r) for r in p1_responses])
    print(f'part one: {p1_ans}')
    p2_responses = parse_multiline(args, lambda x: set.intersection(*x))
    p2_ans = sum([len(r) for r in p2_responses])
    print(f'part two: {p2_ans}')
    # part one: 6551 
    # part two: 3358

if __name__ == '__main__':
    main(sys.argv)