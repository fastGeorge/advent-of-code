import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
    

inputList = getLinesInputFile("day14", "input.txt")

startC = 100
rL = 200
cL = 1000
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

def sandPour2(grid = grid):
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


#One added to make up for the last grain of sand
grains = 1
while sandPour2():
    grains += 1

printGrid(grid)
print(grains)



