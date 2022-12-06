import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile

inputList = getLinesInputFile("day4", "input.txt")



def checkOverlap(line:str):
    line = line.strip()
    pair = line.split(",")
    range1 = [int(i) for i in pair[0].split("-") if i.isdigit()]
    range2 = [int(i) for i in pair[1].split("-") if i.isdigit()]

    if range1[0] <= range2[0] and range1[1] >= range2[1]:
        return True
    elif range1[0] >= range2[0] and range1[1] <= range2[1]:
        return True
    else:
        return False


def checkAnyOverlap(line:str):
    line = line.strip()
    pair = line.split(",")
    range1 = [int(i) for i in pair[0].split("-") if i.isdigit()]
    range2 = [int(i) for i in pair[1].split("-") if i.isdigit()]

    if range1[1] >= range2[0] and range1[0] <= range2[1]:
        return True
    else:
        return False

#Problem1
sum = 0
for line in inputList:
    if checkOverlap(line):
        sum += 1

print("ans1: ", sum)

#Problem2
sum = 0
for line in inputList:
    if checkAnyOverlap(line):
        sum += 1
    
print("ans2: ", sum)