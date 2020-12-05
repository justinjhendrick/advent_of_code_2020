import sys
import numpy as np
from functools import reduce
import operator

class Map:
    def __init__(self, nrow, ncol):
        self.nrow = nrow
        self.ncol = ncol
        self.map = np.zeros((nrow, ncol), dtype=bool)

    def put(self, row, col, is_tree):
        self.map[row, col] = is_tree

    def is_tree(self, row, col):
        return self.map[row, col % self.ncol]


def parse(args):
    with open(args[1], mode='r') as f:
        lines = f.readlines()
        nrow = len(lines)
        ncol = len(lines[0].strip())
        m = Map(nrow, ncol)
        row = 0
        for line in lines:
            for col in range(ncol):
                m.put(row, col, line[col] == '#')
            row += 1
    return m


def how_many_trees_in_line(m, row_step, col_step):
    num_trees = np.uint64(0)
    row = 0
    col = 0
    while row < m.nrow:
        num_trees += (m.is_tree(row, col))
        row += row_step
        col += col_step
    return num_trees


def main(args):
    m = parse(args)
    routes = []
    routes.append(how_many_trees_in_line(m, 1, 1))
    routes.append(how_many_trees_in_line(m, 1, 3))
    routes.append(how_many_trees_in_line(m, 1, 5))
    routes.append(how_many_trees_in_line(m, 1, 7))
    routes.append(how_many_trees_in_line(m, 2, 1))
    print(f'part one: {routes[1]}')
    product = reduce(operator.mul, routes, 1)
    print(f'part two: {product}')
    # part one: 156
    # part two: 3521829480.0 

if __name__ == '__main__':
    main(sys.argv)