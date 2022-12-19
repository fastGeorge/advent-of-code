import sys, os, time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
    

inputList = getLinesInputFile("day14", "input.txt")

startC = 300
rL = 200
cL = 400

def makeGrid(startC = startC, rL = rL, cL = cL):
    grid = []
    for r in range(rL):
        row = []
        for c in range(cL):
            if c == 0:
                if r >= 3:
                    row.append(str(r - 3))
                else:
                    row.append(" ")
            else:
                if r < 3:
                    hund = (startC + c - 1) // 100
                    ten = ((startC + c - 1) - hund * 100) // 10
                    one = (startC + c - 1) % 10
                    if r == 0:
                        row.append(str(hund))
                    if r == 1:
                        row.append(str(ten))
                    if r == 2:
                        row.append(str(one))
                else:
                    row.append(".")
        grid.append(row)
    
    return grid

grid = makeGrid()

def printGrid(grid:list):
    for r in grid:
        line = ""
        for c in r[1:]:
            line += c + " "
        print(line)

def readInput(line:str, startC:int, maxH:int, grid = grid):
    maxH = maxH
    seq = line.split("->")
    for i in range(len(seq) - 1):
        idx1 = [int(k) for k in seq[i].strip().split(",") if k.isdigit()]
        idx2 = [int(k) for k in seq[i + 1].strip().split(",") if k.isdigit()]
        if idx1[0] == idx2[0]:
            hi = max(idx1[1], idx2[1])
            lo = min(idx1[1], idx2[1])
            for r in range(hi + 1 - lo):
                grid[lo + r + 3][idx1[0] - startC + 1] = "#"
        else:
            hi = max(idx1[0], idx2[0])
            lo = min(idx1[0], idx2[0])
            for c in range(hi + 1 - lo):
                grid[idx1[1] + 3][lo + c - startC + 1] = "#"

        maxH = max(maxH, max(idx1[1] + 3, idx2[1] + 3))
    return maxH

def getGrid():
    return grid

maxH = 0
for line in inputList:
    maxH = readInput(line, startC, maxH)

for c in range(len(grid[0])):
    grid[maxH + 2][c] = "#"


def sandPour(grid = grid):
    sR = 3
    sC = 500 - startC + 1
    grid[sR][sC] = "o"
    while sR < len(grid) - 1 and sC > 1 and sC < len(grid[0]) - 1:
        grid[sR][sC] = "."
        if grid[sR + 1][sC] == ".":
            sR += 1
        elif grid[sR + 1][sC - 1] == ".":
            sR += 1
            sC -= 1
        elif grid[sR + 1][sC + 1] == ".":
            sR += 1
            sC += 1
        else:
            grid[sR][sC] = "o"
            return 1
        
        grid[sR][sC] = "o"
    grid[sR][sC] = "."
    return 0

def sandPour2(grid:list):
    sR = 3
    sC = 500 - startC + 1
    grid[sR][sC] = "o"
    while True:
        grid[sR][sC] = "."
        if grid[sR + 1][sC] == ".":
            sR += 1
        elif grid[sR + 1][sC - 1] == ".":
            sR += 1
            sC -= 1
        elif grid[sR + 1][sC + 1] == ".":
            sR += 1
            sC += 1
        else:
            grid[sR][sC] = "o"
            if sC == 500 - startC + 1 and sR == 3:
                return 0
            else:
                return 1
        
        grid[sR][sC] = "o"


# SLOPPY ANIMATION

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

grid = getGrid()



def nbrGrid(grid):
    newGrid = []
    for r in range(len(grid[3:])):
        row = []
        for c in range(len(grid[0][1:])):
            val = None
            if grid[r + 3][c + 1] == ".":
                val = 0
            elif grid[r + 3][c + 1] == "#":
                val = 1
            elif grid[r + 3][c + 1] == "o":
                val = 2
            row.append(val)
        newGrid.append(row)
    return newGrid


arr = np.array(nbrGrid(grid))

plt.ion()

fig = plt.figure()

pixel_plot = plt.imshow(arr, cmap='tab20b', vmin=0, vmax=2)

plt.show()

grains = 0
while sandPour2(grid):
    grains += 1
    if grains % 500 == 0:
        arr = np.array(nbrGrid(grid))
        pixel_plot.set_data(arr)
        fig.canvas.flush_events()

time.sleep(3)

print(grains)