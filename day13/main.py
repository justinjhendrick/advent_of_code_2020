import sys
import math


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_file(filename):
    lines = [line for line in stripped_lines(filename)]
    available_time = int(lines[0])
    buses = [None if bus == 'x' else int(bus) for bus in lines[1].split(',')]
    return available_time, buses


def p1(inputs):
    available_time, buses = inputs
    min_wait = math.inf
    min_bus = None
    for bus in buses:
        if bus == None:
            continue
        waiting = bus - (available_time % bus)
        if waiting < min_wait:
            min_wait = waiting
            min_bus = bus
    return min_wait * min_bus


def get_max_offset(raw_buses):
    '''
    Return the index of the maximum bus id
    '''
    lst = [0 if b == None else int(b) for b in raw_buses]
    return lst.index(max(lst))


def parse(raw_buses, max_offset):
    '''
    Remove Nones and sort by bus number (decreasing)
    Elements are a tuple of bus number and its offset, relative to max_offset
    '''
    buses = []
    for i in range(len(raw_buses)):
        if raw_buses[i] == None:
            continue
        buses.append((raw_buses[i], i - max_offset))
    buses.sort(reverse=True)
    return buses


def simplify(buses):
    '''
    If the bus id is a multiple of the offset, the offset may as well be zero.
    Combine all the zero offset buses and put them at the head of the list.
    '''
    new_buses = []
    conglomerate = 1
    for bus, offset in buses:
        if offset == 0 or bus % abs(offset) == 0:
            conglomerate = math.lcm(conglomerate, bus)
        else:
            new_buses.append((bus, offset))
    return [(conglomerate, 0)] + new_buses


def p2(inputs):
    _, raw_buses = inputs
    max_offset = get_max_offset(raw_buses)
    buses = simplify(parse(raw_buses, max_offset))
    start_time = 0
    while True:
        for bus, offset in buses[1:]:
            if (start_time + offset) % bus != 0:
                break
        else:
            return start_time - max_offset
        start_time += buses[0][0]


def main(args):
    inputs = parse_file(args[1])
    p1_ans = p1(inputs)
    print(f'part one: {p1_ans}')
    p2_ans = p2(inputs)
    print(f'part two: {p2_ans}')
    # part one: 207
    # part two: 530015546283687


if __name__ == '__main__':
    main(sys.argv)
