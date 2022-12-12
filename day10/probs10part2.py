import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day10", "input.txt")

matrix = []
for r in range(6):
    r = []
    for c in range(40):
        r.append(".")
    matrix.append(r)

def draw(cycle:int, x:int, matrix = matrix):
    r = int(cycle/40)
    c = cycle % 40 - 1
    if c == x or c == x - 1 or c == x + 1:
        print(r)
        print(c)
        print("\n")
        matrix[r][c] = "#"

def drawAll():
    for r in matrix:
        line = ""
        for c in r:
            line += c
        print(line)



cycle = 0
x = 1
twentList = []
for line in inputList:
    split = line.split()
    if split[0] == "noop":
        cycle += 1
        draw(cycle, x)
    elif split[0] == "addx":
        cycle += 1
        draw(cycle, x)
        cycle += 1
        draw(cycle, x)
        x += int(split[1])

drawAll()