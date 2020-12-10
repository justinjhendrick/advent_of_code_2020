import sys
import math


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse(filename):
    return [int(line) for line in stripped_lines(filename)]


def count_differences(ratings):
    # assuming ratings is sorted
    result = [0, 0, 0]
    for i in range(1, len(ratings)):
        prv = ratings[i - 1]
        cur = ratings[i]
        diff = cur - prv
        assert diff > 0
        assert diff < 4
        result[diff - 1] += 1
    return result


class AdapterSetCounter:
    '''
    Count all sets of adapters that can charge your device
    '''
    def __init__(self, ratings):
        # assuming ratings is sorted
        self.cache = {}
        self.ratings = ratings

    def run(self):
        return self._permutations(len(self.ratings) - 1)

    def _permutations(self, index):
        if index in self.cache:
            return self.cache[index]
        ans = self._compute(index)
        self.cache[index] = ans
        return ans

    def _compute(self, index):
        if index == 0:
            return 1
        target = self.ratings[index]
        count = 0
        i = index - 1
        while i >= 0 and target - self.ratings[i] < 4:
            count += self._permutations(i)
            i -= 1
        return count


def main(args):
    ratings = parse(args[1])
    ratings.sort()
    # add wall socket and your device
    ratings = [0] + ratings + [(ratings[-1] + 3)]
    diffs = count_differences(ratings)
    p1_ans = diffs[0] * diffs[2]
    print(f'part one: {p1_ans}')
    p2_ans = AdapterSetCounter(ratings).run()
    print(f'part two: {p2_ans}')
    # part one: 2738
    # part two: 74049191673856


if __name__ == '__main__':
    main(sys.argv)
