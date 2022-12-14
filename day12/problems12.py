import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day12", "input.txt")

import heapq
import math


grid = []
rcIdx = []
aList = []
s = tuple()
e = tuple()
for rIdx, line in enumerate(inputList):
    row = []
    for cIdx, letter in enumerate(line):

        if letter == "a" or letter == "S":
            aList.append((rIdx, cIdx))
        
        if letter == "S":
            s = (rIdx, cIdx)
            row.append("a")
        elif letter == "E":
            e = (rIdx, cIdx)
            row.append("z")
        else:
            row.append(letter)
        rcIdx.append((rIdx, cIdx))
    grid.append(row)


def getNeighbors(node:tuple, grid = grid):
    letter = grid[node[0]][node[1]]
    neighbors = []
    if node[0] + 1 < len(grid) and ord(letter) >= ord(grid[node[0] + 1][node[1]]) - 1:
        neighbors.append((node[0] + 1, node[1]))

    if node[0] - 1 >= 0 and ord(letter) >= ord(grid[node[0] - 1][node[1]]) - 1:
        neighbors.append((node[0] - 1, node[1]))

    if node[1] + 1 < len(grid[0]) and ord(letter) >= ord(grid[node[0]][node[1] + 1]) - 1:
        neighbors.append((node[0], node[1] + 1))

    if node[1] - 1 >= 0 and ord(letter) >= ord(grid[node[0]][node[1] - 1]) - 1:
        neighbors.append((node[0], node[1] - 1))
    return neighbors
        
    

def h(current:tuple, end:tuple):

    r = end[0] - current[0]
    c = end[1] - current[1]
    return int(math.sqrt(r * r + c * c))

#def recreatePath()

def aStar(start:tuple, goal:tuple):

    pq = []
    heapq.heappush(pq, (0, start))

    cameFrom = dict()

    gScore = dict()
    for idx in rcIdx:
        gScore[idx] = sys.maxsize
    gScore[start] = 0

    fScore = dict()
    for idx in rcIdx:
        fScore[idx] = sys.maxsize
    fScore[start] = h(start, goal)

    while len(pq) > 0:

        current = heapq.heappop(pq)[1]
        if current[0] == goal[0] and current[1] == goal[1]:
            return gScore[current]
        
        for neighbor in getNeighbors(current):
            
            tentative_G = gScore[current] + 1
            if tentative_G < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_G
                fScore[neighbor] = tentative_G + h(neighbor, goal)
                heapq.heappush(pq, (fScore[neighbor], neighbor))
    
    return None

shortest = sys.maxsize               
for a in aList:
    dist = aStar(a, e)
    if dist != None and dist < shortest:
        shortest = dist

print(shortest)

