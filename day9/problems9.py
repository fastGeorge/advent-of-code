import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day9", "input.txt")

sizeM = 20
matrix = []
for r in range(sizeM):
    cols = []
    for c in range(sizeM):
        cols.append('.')
    matrix.append(cols)

s = [int(sizeM/2), int(sizeM/2)]

knots = []
for k in range(10):
    knots.append([s[0], s[1]])

print(knots)
#h = [s[0], s[1]]
#t = [s[0], s[1]]

def moveTail(h, t):
    difR = h[0] - t[0]
    difC = h[1] - t[1]
    #check = True
    if difR > 1:
        t[0] += 1
        if difC < 0:
            t[1] -= 1
        elif difC > 0:
            t[1] +=1
    elif difR < -1:
        t[0] -= 1
        if difC < 0:
            t[1] -= 1
        elif difC > 0:
            t[1] +=1

    elif difC > 1:
        t[1] += 1
        if difR < 0:
            t[0] -= 1
        elif difR > 0:
            t[0] +=1
        
    elif difC < -1:
        t[1] -= 1
        if difR < 0:
            t[0] -= 1
        elif difR > 0:
            t[0] +=1




def printMatrix():
    for r in range(len(matrix)):
        line = ""
        for c in range(len(matrix[0])):
            line += matrix[r][c]
        print(line)

def clearMatrix():
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            matrix[r][c] = "."
    matrix[s[0]][s[1]] = "s"

tSet = set()
tSet.add(str(knots[9][0]) + "," + str(knots[9][1]))
#matrix[s[0]][s[1]] = "s"
for line in inputList:
    split = line.split()
    
    for n in range(int(split[1])):
        h = knots[0]
        if split[0] == "L":
            h[1] -= 1
        elif split[0] == "R":
            h[1] += 1
        elif split[0] == "U":
            h[0] -= 1
        elif split[0] == "D":
            h[0] += 1
        clearMatrix()
        for i in range(9):
            moveTail(knots[i], knots[i + 1])
            #matrix[knots[i][0]][knots[i][1]] = str(i)
        #printMatrix()
        print("\n")    
        tSet.add(str(knots[9][0]) + "," + str(knots[9][1]))


#printMatrix()
print(tSet)
print(len(tSet))



