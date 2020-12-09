import sys
from collections import defaultdict
import pyparsing as pp


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse(filename):
    grammar = pp.oneOf(['nop', 'acc', 'jmp']) + pp.Combine(pp.oneOf(['+', '-']) + pp.Word(pp.nums))
    result = []
    for line in stripped_lines(filename):
        tokens = grammar.parseString(line)
        result.append([tokens[0], int(tokens[1])])
    return result


def execute(insns):
    visited = set()
    acc = 0
    pc = 0
    finished = True
    while pc < len(insns):
        if pc in visited:
            finished = False
            break
        visited.add(pc)
        insn = insns[pc]
        if insn[0] == 'nop':
            pass
        elif insn[0] == 'acc':
            acc += insn[1]
        elif insn[0] == 'jmp':
            pc += insn[1]
            continue
        pc += 1
    return acc, finished


def alter(insns):
    '''
    Make exactly one swap per new instruction list
    '''
    last_swap = -1
    while last_swap < len(insns):
        i = last_swap + 1
        while i < len(insns):
            if insns[i][0] == 'nop':
                insns[i][0] = 'jmp'
                last_swap = i
                break
            elif insns[i][0] == 'jmp':
                insns[i][0] = 'nop'
                last_swap = i
                break
            i += 1
        yield insns
        # undo last swap
        if insns[last_swap][0] == 'nop':
            insns[last_swap][0] = 'jmp'
        elif insns[last_swap][0] == 'jmp':
            insns[last_swap][0] = 'nop'


def find_swap(insns):
    for altered_insns in alter(insns):
        acc, finished = execute(altered_insns)
        if finished:
            return acc
    return None
        

def main(args):
    insns = parse(args[1])
    p1_ans, _ = execute(insns)
    print(f'part one: {p1_ans}')
    p2_ans = find_swap(insns)
    print(f'part two: {p2_ans}')
    # part one: 1528
    # part two: 640


if __name__ == '__main__':
    main(sys.argv)