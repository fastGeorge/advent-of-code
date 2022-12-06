import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
from collections import deque

inputList = getLinesInputFile("day5", "input.txt")

def makeCrateArray(crateList:list):
    crateArray = list()

    for line in crateList:
        length = len(line)
        #nbrStacks = length/4
        lineArray = list()
        idx:int = 1
        while idx < length:
            #lineArray.append(line[idx:idx+3])
            lineArray.append(line[idx])
            idx += 4

        crateArray.append(lineArray)

    return crateArray

def makeStacks(crateArray:list):
    length = len(crateArray[0])
    stacks = list()

    while length > 0:
        stacks.append(deque())
        length -= 1
    for line in reversed(crateArray):
        i = 0
        for crate in line:
            if(len(crate.strip()) > 0):
                stacks[i].append(crate)
            i += 1
    
    return stacks

def followInst(inst:str, stacks:list):
    nbrs = [int(i) for i in inst.split() if i.isdigit()]

    op = 0
    while op < nbrs[0]:
        stacks[nbrs[2] - 1].append(stacks[nbrs[1] - 1].pop())
        op += 1

def followInstProb2(inst:str, stacks:list):
    nbrs = [int(i) for i in inst.split() if i.isdigit()]

    op = 0
    crateHolder = deque()
    while op < nbrs[0]:

        crateHolder.append(stacks[nbrs[1] - 1].pop())
        op += 1

    while len(crateHolder) > 0:
        stacks[nbrs[2] - 1].append(crateHolder.pop())



stacks = makeStacks(makeCrateArray(inputList[0:8]))

for line in inputList[10:]:
    followInstProb2(line, stacks)


topCrates = list()
for stack in stacks:
    topCrates.append(stack.pop())

res = ""
print(res.join(topCrates))



