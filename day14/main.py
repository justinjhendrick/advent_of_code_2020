import sys


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()

class Insn:
    def __init__(self, loc=None, val=None, mask=None):
        self.loc = loc
        self.val = val
        self.mask = mask


def parse_file(filename):
    insns = []
    for line in stripped_lines(filename):
        if line[0:4] == 'mask':
            mask = line[7:]
            assert len(mask) == 36
            insns.append(Insn(mask=mask))
        else:
            open_bracket = line.index('[')
            loc_start = open_bracket + 1
            loc_end = line.index(']')
            loc = int(line[loc_start:loc_end])
            equals = line.index('=')
            val_start = equals + 2
            val = int(line[val_start:])
            insns.append(Insn(loc=loc, val=val))
    return insns


def to_binary(length, v):
    bin_val = bin(v)[2:]
    return ('0' * (length - len(bin_val))) + bin_val


def to_decimal(b):
    return int(''.join(b), 2)


def apply_mask_p1(mask, val):
    bin_val = to_binary(len(mask), val)
    result = []
    for i in range(len(mask)):
        if mask[i] == 'X':
            result.append(bin_val[i])
        else:
            result.append(mask[i])
    return to_decimal(result)


def p1(inputs):
    memory = {}
    mask = None
    for insn in inputs:
        if insn.mask is not None:
            mask = insn.mask
        else:
            assert mask is not None
            memory[insn.loc] = apply_mask_p1(mask, insn.val)
    return sum([v for v in memory.values()])


def apply_mask_p2(mask, loc):
    bin_loc = to_binary(len(mask), loc)
    for b in apply_mask_p2_helper(mask, bin_loc):
        yield to_decimal(b)


def apply_mask_p2_helper(mask, bin_loc):
    result = []
    for i in range(len(mask)):
        if mask[i] == '0':
            result.append(bin_loc[i])
        elif mask[i] == '1':
            result.append('1')
        else:
            for rest in apply_mask_p2_helper(mask[i + 1:], bin_loc[i + 1:]):
                yield result + ['0'] + rest
                yield result + ['1'] + rest
            break
    else:
        yield result


def p2(inputs):
    memory = {}
    for insn in inputs:
        if insn.mask is not None:
            mask = insn.mask
        else:
            assert mask is not None
            for loc in apply_mask_p2(mask, insn.loc):
                memory[loc] = insn.val
    return sum([v for v in memory.values()])


def main(args):
    inputs = parse_file(args[1])
    p1_ans = p1(inputs)
    print(f'part one: {p1_ans}')
    p2_ans = p2(inputs)
    print(f'part two: {p2_ans}')
    # part one: 16003257187056
    # part two: 3219837697833


if __name__ == '__main__':
    main(sys.argv)