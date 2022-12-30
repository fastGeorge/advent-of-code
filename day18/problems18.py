import sys, os, time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day18", "input.txt")

def checkSides(xyz:tuple, cubes:set):
    sides = 0
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    if (x + 1, y, z) in cubes:
        sides += 1
    if (x - 1, y, z) in cubes:
        sides += 1
    if (x, y + 1, z) in cubes:
        sides += 1
    if (x, y - 1, z) in cubes:
        sides += 1
    if (x, y, z + 1) in cubes:
        sides += 1
    if (x, y, z - 1) in cubes:
        sides += 1
    return sides


cubes = set()
sides = 0
for i, line in enumerate(inputList):
    split = line.split(",")
    xyz = (int(split[0]), int(split[1]), int(split[2]))
    cubes.add(xyz)
    sides += checkSides(xyz, cubes)

firstPart = len(inputList) * 6 - (sides * 2)
print(firstPart)

#===================PART 2===============================
maxX = 0
maxY = 0
maxZ = 0

for s in cubes:
    if s[0] > maxX:
        maxX = s[0]
    if s[1] > maxY:
        maxY = s[1]
    if s[2] > maxZ:
        maxZ = s[2]

maxCord = (maxX, maxY, maxZ)

import numpy as np

grid = np.zeros((maxX + 20, maxY + 20, maxZ + 20), np.int8)

for s in cubes:
    grid[s[0] + 10 ,s[1] + 10 ,s[2] + 10] = 1

def getNeighbors(current:tuple):
    neighbors = []
    x = current[0]
    y = current[1]
    z = current[2]

    if x > 0:
        neighbors.append((x - 1, y, z))
    if x < maxX + 19:
        neighbors.append((x + 1, y, z))
    
    if y > 0:
        neighbors.append((x, y - 1, z))
    if y < maxY + 19:
        neighbors.append((x, y + 1, z))
    
    if z > 0:
        neighbors.append((x, y, z - 1))
    if z < maxZ + 19:
        neighbors.append((x, y, z + 1))
    
    return neighbors

def findEdges(start:tuple, grid):
    edges = 0
    visited = set()

    queue = []
    queue.append(start)
    visited.add(start)

    while queue:

        current = queue.pop(0)

        for n in getNeighbors(current):
            if grid[n] == 1:
                edges += 1
            elif n not in visited:
                visited.add(n)
                queue.append(n)

    return edges


print(findEdges((0,0,0), grid))

#===============================================================

import matplotlib.pyplot as plt

plt.ion()

fig = plt.figure()

plot = plt.imshow(grid[:,:,0], cmap="tab20b", vmin=0, vmax=1)

plt.show()

for z in range(maxZ + 20):
    time.sleep(0.1)
    plot.set_data(grid[:,:, z])
    fig.canvas.flush_events()

plt.ioff()
plt.show()




    