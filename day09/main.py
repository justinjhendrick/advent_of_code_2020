import sys


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


class Ring:
    def __init__(self, mx):
        self.cur = 0
        self.max = mx
        self.data = []
    
    def append(self, val):
        if len(self.data) < self.max:
            self.data.append(val)
        else:
            self.data[self.cur] = val
            self.cur = (self.cur + 1) % self.max

    def get(self):
        if len(self.data) < self.max:
            return None
        return self.data


def can_find_sum(target, candidates):
    for c1 in candidates:
        for c2 in candidates:
            if c1 == c2:
                continue
            if c1 + c2 == target:
                return True
    return False


def parse(filename):
    return [int(line) for line in stripped_lines(filename)]


def first_without_sum(window_size, vals):
    ring = Ring(window_size)
    for v in vals:
        if ring.get() is not None and not can_find_sum(v, ring.get()):
            return v
        ring.append(v)


def find_contiguous_summing_to(target, vals):
    window = []
    i = 0
    while i < len(vals):
        sm = sum(window)
        if sm == target:
            return min(window) + max(window)
        elif sm < target:
            v = vals[i]
            i += 1
            window.append(v)
        elif sm > target:
            del window[0]


def main(args):
    vals = parse(args[1])
    window_size = int(args[2])
    p1_ans = first_without_sum(window_size, vals)
    print(f'part one: {p1_ans}')
    p2_ans = find_contiguous_summing_to(p1_ans, vals)
    print(f'part two: {p2_ans}')
    # part one: 2089807806
    # part two: 245848639

if __name__ == '__main__':
    main(sys.argv)
