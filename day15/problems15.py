import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day15", "input.txt")

import numpy as np


sbPairs = []
for line in inputList:
    line = line.split(":")
    pair = []
    for l in line:
        comma = l.split(",")
        x = int(comma[0].split("=")[-1])
        y = int(comma[1].split("=")[-1])
        pair.append((y, x))
    sbPairs.append(pair)

#Sensor 0 beacon 1
print(sbPairs)

# 0 is uncovered
# 1 is sensor
# 2 is beacon
# 3 is covered

#row and col don't start at zero in dataset:
negRow = 10
negCol = 10

grid = np.zeros((40, 40), np.int32)

def manDist(s:tuple, b:tuple):
    

    r = s[0] - b[0]
    c = s[1] - b[1]
    return abs(r) + abs(c)

def checkSize(s:tuple, dist:int, grid = grid, negRow = negRow, negCol = negCol):
    inc = 40
    #newGrid = None
    if s[0] + negRow - dist < 0:
        extra = np.zeros((inc, len(grid[0])), np.int32)
        grid = np.concatenate((extra, grid), axis=0)
        negRow += inc
    if s[0] + negRow + dist >= len(grid):
        extra = np.zeros((inc, len(grid[0])), np.int32)
        grid = np.concatenate((grid, extra), axis=0)
    if s[1] + negCol - dist < 0:
        extra = np.zeros((len(grid), inc), np.int32)
        grid = np.concatenate((extra, grid), axis=1)
        negCol += inc
    if s[1] + negRow + dist >= len(grid[0]):
        extra = np.zeros((len(grid), inc), np.int32)
        grid = np.concatenate((grid, extra), axis=1)

    
        
negCol = 2000000
soughtRow = np.zeros(7000000, np.int8)


for pair in sbPairs:
    s = pair[0]
    b = pair[1]
    if b[0] == 2000000:
        soughtRow[b[1] + negCol] = 2
    dist = manDist(s, b)
    distToRow = manDist(s, (2000000, s[1]))
    if dist >= distToRow:
        for i in range(dist + 1 - distToRow):
            if soughtRow[s[1] + negCol - i] != 2:
                soughtRow[s[1] + negCol - i] = 3
            if soughtRow[s[1] + negCol + i] != 2:
                soughtRow[s[1] + negCol + i] = 3

print(soughtRow)
sum = 0
for k, i in enumerate(soughtRow):
    if k - negCol >= 0 and k <= 6000000:
        if i == 0:
            print(k - negCol)
    if i == 3:
        sum += 1

print(sum)


