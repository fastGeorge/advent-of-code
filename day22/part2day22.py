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

np_grid
sections = []
top_left_sec = []
r = 0
c = 0

while r < len(np_grid):
    while c < len(np_grid[0]):
        print(r, c)
        if np_grid[r][c] != 0:
            top_left_sec.append((r,c))
            sections.append(np_grid[r:r+50,c:c+50])
        c += 50
    c = 0
    r += 50



def adjacent(sec:int):

    if sec == 0:
        return {
            'R': "2LS",
            'L': "4LF",
            'D': "3US",
            'U': "6LR"
        }
    elif sec == 1:
        return {
            'R': "5RF",
            'L': "1RS",
            'D': "3RR",
            'U': "6DS"
        }
    elif sec == 2:
        return {
            'R': "2DR",
            'L': "4UR",
            'D': "5US",
            'U': "1DS"

        }
    elif sec == 3:
        return {
            'R': "5LS",
            'L': "1LF",
            'D': "6US",
            'U': "3LR"
        }
    elif sec == 4:
        return {
            'R': "2RF",
            'L': "4RS",
            'D': "6RR",
            'U': "3DS"
        }
    elif sec == 5:
        return {
            'R': "5DR",
            'L': "1UR",
            'D': "2US",
            'U': "4DS"
        }



def move(sections, sec_num:int, dirct, pos:tuple):
    next_pos = pos
    code = ""
    sec = sections[sec_num]
    no_moves = False

    #right
    if dirct == 0:

        if pos[1] + 1 >= len(sec[0]):
            code = adjacent(sec_num)['R']
        else:
            next_pos = (next_pos[0], next_pos[1] + 1)
    #down
    elif dirct == 1:

        if pos[0] + 1 >= len(sec):
            code = adjacent(sec_num)['D']
        else:
            next_pos = (next_pos[0] + 1, next_pos[1])
    #left
    elif dirct == 2:

        if pos[1] - 1 < 0:
            code = adjacent(sec_num)['L']
        else:
            next_pos = (next_pos[0], next_pos[1] - 1)
    #up
    elif dirct == 3:

        if pos[0] - 1 < 0:
            code = adjacent(sec_num)['U']
        else:
            next_pos = (next_pos[0] - 1, next_pos[1])
    
    if code == "":
        if sec[next_pos] == 1 or sec[next_pos] == 3:
            sec[pos] = 3
            sec[next_pos] = 4
            pos = next_pos
        else:
            no_moves = True
    else:
        new_sec_num = int(code[0]) - 1
        new_sec = sections[new_sec_num]
        border = code[1]

        #Reverse
        if code[2] == 'R':
            next_pos = (pos[1], pos[0]) 
        #Flip  
        elif code[2] == 'F':
            
            next_pos = (49 - pos[0], 49 - pos[1])
            print(next_pos)

        if border == 'R':
            next_pos = (next_pos[0], 49)
            dirct_ = 2
        elif border == 'L':
            next_pos = (next_pos[0], 0)
            dirct_ = 0
        elif border == 'D':
            next_pos = (49, next_pos[1])
            dirct_ = 3
        elif border == 'U':
            next_pos = (0, next_pos[1])
            dirct_ = 1


        if new_sec[next_pos] == 1 or new_sec[next_pos] == 3:
            sec[pos] = 3
            new_sec[next_pos] = 4
            pos = next_pos
            dirct = dirct_
            sec_num = new_sec_num
        else:
            no_moves = True

    return sec_num, dirct, pos, no_moves


inst_list = []
inst = inputList[-1].strip()
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

sec_num = 0
pos = (0,0)
dirct = 0

import matplotlib.pyplot as plt

f, sub_arr = plt.subplots(3,2)
sides = []
for i, section in enumerate(sections):
    sides.append(sub_arr[i // 2, i % 2].imshow(section, cmap='tab20b', vmin=0, vmax=4))
    sub_arr[i // 2, i % 2].set_title(i)

for moves, lr in inst_list:
    while moves > 0:
        sec_num, dirct, pos, no_moves = move(sections, sec_num, dirct, pos)
        moves -= 1
        if no_moves:
            moves = 0
    else:
        if lr == "R":
            dirct = (dirct + 1) % 4
        elif lr == "L":
            dirct = (dirct - 1) % 4


for i, section in enumerate(sections):
        sides[i].set_data(section)
        f.canvas.flush_events()
            
print(pos)
print(sec_num)
print(dirct)

print((pos[0] + top_left_sec[sec_num][0] + 1) * 1000 + (pos[1] + top_left_sec[sec_num][1] + 1) * 4 + dirct)
plt.show()

