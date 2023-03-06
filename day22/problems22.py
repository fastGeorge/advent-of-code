import sys, os, time, math
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFileNoStrip
inputList = getLinesInputFileNoStrip("day22", "input.txt")

grid = []
max_len = 0
for line in inputList:
    pos_line = list(line)[:-1]
    max_len = max(max_len, len(pos_line))
    if len(pos_line) == 0:
        break
    else:
        row = []
        for ch in pos_line:
            if ch == " ":
                row.append(0)
            elif ch == ".":
                row.append(1)
            elif ch == "#":
                row.append(2)

        grid.append(row)

np_grid = np.zeros((len(grid),max_len), np.int8)


for r, rval in enumerate(grid):
    for c, cval in enumerate(rval):
        np_grid[r, c] = cval


print(np_grid)





def move(dirct:int, pos:tuple, np_grid):
    next_pos = pos
    #Right
    if dirct == 0:
        
        if pos[1] + 1 >= len(np_grid[0]) or np_grid[pos[0], pos[1] + 1] == 0:
            if np_grid[pos[0], 0] != 0:
                next_pos = (pos[0], 0)
            else:
                next_pos = (pos[0], np.where(np_grid[pos[0],:] != 0)[0][0])
        else:
            next_pos = (pos[0], pos[1] + 1)
    #Down
    elif dirct == 1:
        
        if pos[0] + 1 >= len(np_grid) or np_grid[pos[0] + 1, pos[1]] == 0:
            if np_grid[0, pos[1]] != 0:
                next_pos = (0, pos[1])
            else:
                next_pos = (np.where(np_grid[0:,pos[1]] != 0)[0][0], pos[1])
        else:
            next_pos = (pos[0] + 1, pos[1])
    #Left
    elif dirct == 2:
        
        if pos[1] - 1 < 0 or np_grid[pos[0], pos[1] - 1] == 0:
            if np_grid[pos[0], len(np_grid[0]) - 1] != 0:
                next_pos = (pos[0], len(np_grid[0]) - 1)
            else:
                next_pos = (pos[0], pos[1] + np.where(np_grid[pos[0],pos[1]:] == 0)[0][0] - 1)
        else:
            next_pos = (pos[0], pos[1] - 1)
    #Up
    elif dirct == 3:
        
        if pos[0] - 1 < 0 or np_grid[pos[0] - 1, pos[1]] == 0:
            print("part1 get")
            if np_grid[len(np_grid) - 1, pos[1]] != 0:
                next_pos = (len(np_grid) - 1, pos[1])
            else:
                print("part2 get")
                next_pos = (pos[0] + np.where(np_grid[pos[0]:,pos[1]] == 0)[0][0] - 1, pos[1])
        else:
            next_pos = (pos[0] - 1, pos[1])
    
    if np_grid[next_pos] == 1 or np_grid[next_pos] == 3:
        np_grid[pos] = 3
        np_grid[next_pos] = 4
        pos = next_pos

    return pos, np_grid 


inst = inputList[-1].strip()

dirct = 0

#Set STARTING POSISTION

pos = (0, np.where(np_grid[0] == 1)[0][0])

inst_list = []

print(inst)

nbr_str = ""
for i in inst:
    if i.isdigit():
        nbr_str += i
    else:
        inst_tup = (int(nbr_str), i)
        nbr_str = ""
        inst_list.append(inst_tup)
else:
    if nbr_str != "":
        print("gets here")
        inst_list.append((int(nbr_str), "0"))

print(inst_list)

import matplotlib.pyplot as plt

plt.ion()

fig = plt.figure()

pixel_plot = plt.imshow(np_grid, cmap='tab20b', vmin=0, vmax=4)

plt.show()
print(inst_list[-1])
for moves, lr in inst_list:
    #print(moves, lr)
    while moves > 0:
        #print(dirct)
        pos, np_grid = move(dirct, pos, np_grid)
        moves -= 1
        pixel_plot.set_data(np_grid)
        fig.canvas.flush_events()
        # time.sleep(0.5)
    else:
        if lr == "R":
            dirct = (dirct + 1) % 4
        elif lr == "L":
            dirct = (dirct - 1) % 4
        #else:
        #    dirct = dirct
plt.ioff()
plt.show()
print(np_grid)
print(pos[0] + 1, pos[1] + 1, dirct)
print(1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + dirct)






    
