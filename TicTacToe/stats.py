#!/usr/bin/python
# -*- coding: utf8 -*-"

import copy

all_void_grids = []

def are_equivalents(grid1, grid2):
    # First diag symmetry: Exchange i & j
    same = True
    for i in range(3):
        for j in range(3):
            if grid1[i][j] != grid2[j][i]:
                same = False
    if same:
        return True
    # Second diag symmetry: TODO: Easy computation?
    mapping = {
        (0, 0): (2, 2),
        (0, 1): (1, 2),
        (0, 2): (0, 2),
        (1, 0): (2, 1),
        (1, 1): (1, 1),
        (1, 2): (0, 1),
        (2, 0): (2, 0),
        (2, 1): (1, 0),
        (2, 2): (0, 0),
    }
    same = True
    for i in range(3):
        for j in range(3):
            m = mapping[(i,j)]
            if grid1[i][j] != grid2[m[0]][m[1]]:
                same = False
    if same:
        return True
    # Vertical axis: i / 2-i, Same j
    same = True
    for i in range(3):
        for j in range(3):
            if grid1[i][j] != grid2[2-i][j]:
                same = False
    if same:
        return True
    # Horizontal axis: Same i, j / 2-j
    same = True
    for i in range(3):
        for j in range(3):
            if grid1[i][j] != grid2[i][2-j]:
                same = False
    if same:
        return True
    return False

def filter_out_symmetries(grid):
    result = []
    for i in range(len(grid)):
        ignore = False
        for j in range(i):
            if are_equivalents(grid[i], grid[j]):
                ignore = True
                break
        if not ignore:
            result.append(grid[i])
    return result

def display_grid(grid):
    players = [" ", "X", "O"]
    print("\n".join(["|".join([players[g] for g in line]) for line in grid]))
    print("")

def verify_grid(grid):
    for i in range(3):
        if grid[i][0] == grid[i][1] and grid[i][0] == grid[i][2]:
            return False
    for j in range(3):
        if grid[0][j] == grid[1][j] and grid[0][j] == grid[2][j]:
            return False
    if grid[0][0] == grid[1][1] and grid[0][0] == grid[2][2]:
        return False
    if grid[0][2] == grid[1][1] and grid[0][2] == grid[2][0]:
        return False
    print(grid)
    all_void_grids.append(copy.deepcopy(grid))
    return True

def try_next(grid, i, j, cnt, remaining):
    if remaining == (0, 0):
        if verify_grid(grid):
            return cnt + 1
        else:
            return cnt
    nextj = j+1
    nexti = i
    if nextj == 3:
        nextj = 0
        nexti += 1
    if remaining[0]:
        grid[i][j] = 1
        cnt = try_next(grid, nexti, nextj, cnt, (remaining[0]-1, remaining[1]))
    if remaining[1]:
        grid[i][j] = 2
        cnt = try_next(grid, nexti, nextj, cnt, (remaining[0], remaining[1]-1))
    return cnt

def count_null_grid():
    grid = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
    try_next(grid, 0, 0, 0, (5, 4))

if __name__ == '__main__':
    count_null_grid()
    print("All void grids:")
    for g in all_void_grids:
        print(g)
    uniq = filter_out_symmetries(all_void_grids)
    print("Unique void grids:")
    for g in uniq:
        display_grid(g)
