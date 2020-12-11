import sys
import numpy as np


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse_file(filename):
    lines = [line for line in stripped_lines(filename)]
    nrow = len(lines)
    ncol = len(lines[0])
    grid = np.zeros((nrow, ncol))
    for r in range(nrow):
        for c in range(ncol):
            seat = lines[r][c]
            if seat == 'L':
                grid[r][c] = 1
            elif seat == '#':
                grid[r][c] = 2
    return grid


def get(grid, r, c):
    nrow, ncol = grid.shape
    if r < 0 or c < 0 or r >= nrow or c >= ncol:
        return 0
    return grid[r][c]


def adjs_occupied(grid, row, col):
    count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if r == row and c == col:
                continue
            if get(grid, r, c) == 2:
                count += 1
    return count


def look(grid, rows, cols):
    # if rows or cols is an int, create a repeating list of the appropriate length
    #
    # gotcha: reversed() creates an iterator, which can only be iterated through
    # once. Convert to a list to avoid that problem
    if isinstance(cols, int):
        rows = list(rows)
        c = cols
        cols = [c for _ in rows]
    elif isinstance(rows, int):
        cols = list(cols)
        r = rows
        rows = [r for _ in cols]
    else:
        rows = list(rows)
        cols = list(cols)

    for r, c in zip(rows, cols):
        v = get(grid, r, c)
        if v == 2:
            return 1
        elif v == 1:
            return 0
    return 0

def visible_occupied(grid, row, col):
    nrow, ncol = grid.shape
    count = 0

    # straights
    count += look(grid, range(row + 1, nrow), col)
    count += look(grid, reversed(range(row)), col)
    count += look(grid, row, range(col + 1, ncol))
    count += look(grid, row, reversed(range(col)))

    # diagonals
    count += look(grid, range(row + 1, nrow), range(col + 1, ncol))
    count += look(grid, reversed(range(row)), range(col + 1, ncol))
    count += look(grid, range(row + 1, nrow), reversed(range(col)))
    count += look(grid, reversed(range(row)), reversed(range(col)))
    
    return count


def count_occupied(grid):
    nrow, ncol = grid.shape
    count = 0
    for r in range(nrow):
        for c in range(ncol):
            if grid[r][c] == 2:
                count += 1
    return count


def simulate(grid, sit_condition, stand_condition):
    changed = True
    nrow, ncol = grid.shape
    new_grid = np.zeros(grid.shape)
    while changed:
        changed = False
        for r in range(nrow):
            for c in range(ncol):
                if grid[r][c] == 1 and sit_condition(grid, r, c):
                    changed = True
                    new_grid[r][c] = 2
                elif grid[r][c] == 2 and stand_condition(grid, r, c):
                    changed = True
                    new_grid[r][c] = 1
                else:
                    new_grid[r][c] = grid[r][c]
        grid = new_grid
        new_grid = np.zeros(grid.shape)
    return count_occupied(grid)


def main(args):
    inputs = parse_file(args[1])
    p1_ans = simulate(
        inputs,
        lambda grid, r, c: adjs_occupied(grid, r, c) == 0,
        lambda grid, r, c: adjs_occupied(grid, r, c) >= 4,
    )
    print(f'part one: {p1_ans}')
    p2_ans = simulate(
        inputs,
        lambda grid, r, c: visible_occupied(grid, r, c) == 0,
        lambda grid, r, c: visible_occupied(grid, r, c) >= 5,
    )
    print(f'part two: {p2_ans}')


if __name__ == '__main__':
    main(sys.argv)
