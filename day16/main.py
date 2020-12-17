import sys


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_ranges(range1, range2):
    def bounds(r):
        splitted = r.split('-')
        return int(splitted[0]), int(splitted[1])
    lo1, hi1 = bounds(range1)
    lo2, hi2 = bounds(range2)
    return lambda x: (x >= lo1 and x <= hi1) or (x >= lo2 and x <= hi2)


def parse_ticket(line):
    return [int(v) for v in line.split(',')]


def parse_file(filename):
    state = 0
    rules = {}
    nearby_tickets = []
    for line in stripped_lines(filename):
        if line == '':
            state += 1
            continue
        if line == 'your ticket:' or line == 'nearby tickets:':
            continue
        if state == 0:
            key_end = line.index(':')
            key = line[0:key_end]
            range1_end = line.index(' or ')
            range1 = line[key_end + 2: range1_end]
            range2 = line[range1_end + 4:]
            check_range = parse_ranges(range1, range2)
            rules[key] = check_range
        elif state == 1:
            your_ticket = parse_ticket(line)
        else:
            nearby_tickets.append(parse_ticket(line))
    return rules, your_ticket, nearby_tickets


def validate(rules, value):
    return any(rule(value) for rule in rules.values())


def p1(rules, nearby_tickets):
    invalid_sum = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        valid = True
        for value in ticket:
            if not validate(rules, value):
                valid = False
                invalid_sum += value
        if valid:
            valid_tickets.append(ticket)
    return invalid_sum, valid_tickets


def possible_columns(key, rule, tickets, ncol):
    result = []
    for column in range(ncol):
        if all(rule(ticket[column]) for ticket in tickets):
            result.append(column)
    return result


def get_column_map(rules, valid_tickets):
    ncol = len(valid_tickets[0])
    possibles = []
    # figure out which columns could satisfy which rules
    for key, rule in rules.items():
        columns = possible_columns(key, rule, valid_tickets, ncol)
        possibles.append((columns, key))

    # sort by number of possible columns so that we can satisfy
    # the most constrained rules first
    possibles.sort(key=lambda a: len(a[0]))
    column_map = {}
    taken_columns = set()
    for columns, key in possibles:
        for column in columns:
            if column not in taken_columns:
                column_map[key] = column
                taken_columns.add(column)
                break
    assert len(column_map) == ncol
    return column_map


def p2(rules, your_ticket, valid_tickets):
    column_map = get_column_map(rules, valid_tickets)
    result = 1
    for key, col in column_map.items():
        if key.find('departure') == 0:
            result *= your_ticket[col]
    return result


def main(args):
    inputs = parse_file(args[1])
    rules, your_ticket, nearby_tickets = inputs
    p1_ans, valid_tickets = p1(rules, nearby_tickets)
    print(f'part one: {p1_ans}')
    p2_ans = p2(rules, your_ticket, valid_tickets)
    print(f'part two: {p2_ans}')
    # part one: 25788
    # part two: 3902565915559


if __name__ == '__main__':
    main(sys.argv)
