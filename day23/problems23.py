import sys, os, time, math
import numpy as np
from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFileNoStrip
inputList = getLinesInputFileNoStrip("day23", "input.txt")

elf_pos = []

for r, line in enumerate(inputList):
    for c, char in enumerate(line):
        if char == "#":
            elf_pos.append((r,c))

print(elf_pos)

grid = np.zeros((len(inputList), len(inputList[0])), np.int8)
print(len(grid), len(grid[0]))

import matplotlib.pyplot as plt

plt.ion()

fig = plt.figure()

pixel_plot = plt.imshow(grid, cmap='tab20b', vmin=0, vmax=1)

for elf in elf_pos:
        grid[elf] = 1

print(grid)
pixel_plot.set_data(grid)
fig.canvas.flush_events()

plt.show()

grid = np.zeros((len(grid), len(grid[0])), np.int8)

print("=========================================")

check_order = deque([[(-1, -1), (-1, 0), (-1, 1)],
                      [(1, -1), (1, 0), (1, 1)],
                      [(-1, -1), (0, -1), (1, -1)],
                      [(-1, 1), (0, 1), (1, 1)]])

sur_check = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1), (1, 0), (1, 1)]

#YOU FORGOT THE CONDITION WHERE ONLY ELVES THAT HAVE SOMEONE AROUND THEM MOVES!
has_moved = True
turn = 0
while has_moved:
    turn += 1

    test_pos = []
    #every elf checks
    for elf in elf_pos:
        for check in sur_check:
            if elf_pos.count(tuple(np.add(elf, check))) > 0:
                break
        else:
            test_pos.append(elf)
            continue
        for check_comp in check_order:
            for check in check_comp:
                empty_check = tuple(np.add(elf, check))
                if elf_pos.count(empty_check) > 0:
                    break
            else:
                test_pos.append(tuple(np.add(elf, check_comp[1])))
                break
        else:
            test_pos.append(elf)

    for idx in range(len(test_pos)):
        if test_pos[idx] != elf_pos[idx]:
            break
    else:
        has_moved = False
    new_pos = []
    #check if max one per square
    for elf_idx, e_pos in enumerate(test_pos):
        if test_pos.count(e_pos) > 1:
            new_pos.append(elf_pos[elf_idx])
        else:
            new_pos.append(e_pos)

    elf_pos = new_pos[:]

    if len([tuple for elf in elf_pos if elf[0] < 0]) > 0:
        for idx, elf in enumerate(elf_pos):
            elf_pos[idx] = tuple(np.add(elf, (1, 0)))
    if len([tuple for tuple in elf_pos if tuple[1] < 0]) > 0:
        for idx, elf in enumerate(elf_pos):
            elf_pos[idx] = tuple(np.add(elf, (0, 1)))

    if turn % 20 == 0:
        print(turn)
        south = elf_pos[0][0]
        east = elf_pos[0][1]

        for elf in elf_pos:
            south = max(south, elf[0])
            east = max(east, elf[1])

        grid = np.zeros((south + 1, east + 1), np.int8)
        for elf in elf_pos:
            grid[elf] = 1


        pixel_plot.set_data(grid)
        fig.canvas.flush_events()

    to_move = check_order.popleft()
    check_order.append(to_move)


plt.ioff()
plt.show()

print("TURN: ")
print(turn)


north = elf_pos[0][0]
south = elf_pos[0][0]
west = elf_pos[0][1]
east = elf_pos[0][1]

for elf in elf_pos:
    north = min(north, elf[0])
    south = max(south, elf[0])
    west = min(west, elf[1])
    east = max(east, elf[1])

a = (south - north) + 1
b = east - west + 1
c = len(elf_pos)

print(a, b)
print(a * b)
print((a * b) - c)



