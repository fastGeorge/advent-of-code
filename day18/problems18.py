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

print(len(inputList))
cubes = set()
sides = 0
for i, line in enumerate(inputList):
    if i % 500 == 0:
        print(i)
    split = line.split(",")
    xyz = (int(split[0]), int(split[1]), int(split[2]))
    cubes.add(xyz)
    sides += checkSides(xyz, cubes)

print(len(inputList) * 6 - (sides * 2))
    