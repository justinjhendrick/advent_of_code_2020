import sys

'''
https://adventofcode.com/2020/day/1
'''

def parse(args):
    input_nums = []
    with open(args[1], mode='r') as f:
       for line in f.readlines():
           input_nums.append(int(line.strip()))
    return input_nums


def find2(input_nums, target):
    '''
    Find 2 numbers (assumed positive ints) in input_nums that sum to target. Return their product
    '''
    search_for = set()
    for v in input_nums:
        if v > target:
            continue
        if v in search_for:
            return (target - v) * v
        search_for.add(target - v)
    return None


def find3(input_nums, target):
    '''
    Find 3 numbers (assumed positive ints) in input_nums that sum to target. Return their product
    '''
    for v in input_nums:
        if v > target:
            continue
        result = find2(input_nums, target - v)
        if result is not None:
            return v * result
    return None


def main(args):
    input_nums = parse(args)
    print("part one: {}".format(find2(input_nums, 2020)))
    print("part two: {}".format(find3(input_nums, 2020)))
    # part one: 842016
    # part two: 9199664    


if __name__ == '__main__':
    main(sys.argv)