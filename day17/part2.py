import sys, os, time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day17", "input.txt")

import numpy as np

shapes = {
    "-": np.array([[1, 1, 1, 1]]),
    "+": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    "J": np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]]),
    "|": np.array([[1], [1], [1], [1]]),
    "¤": np.array([[1, 1], [1, 1]])
}
winds = ""
for line in inputList:
    winds += line


def getStart(shape):
    s = shapes[shape]

    bottom = len(s) - 1
    leftCond = np.zeros((len(s), 2), np.int8)
    start = np.concatenate((leftCond, s), axis=1)
    right = len(start[0]) - 1
    start = np.concatenate((start, np.zeros((len(s), 7 - len(start[0])), np.int8)), axis=1)

    leftEd = []
    rightEd = []
    for i, r in enumerate(start):
        leftEd.append([i, np.argmax(r>0)])
        rev = r[::-1]
        rightEd.append([i, len(rev) - 1 - np.argmax(rev>0)])

    start = np.concatenate((start, np.zeros((3, 7), np.int8)))

    botEd = []
    for c in range(len(start[0])):
        arr = start[:, c]
        arr = arr[::-1]

        rowBot = np.argmax(arr>0)
        if rowBot:
            botEd.append([len(arr) - 1 - rowBot, c])

    
    return start, (0, bottom, 2, right), [np.array(botEd), np.array(leftEd), np.array(rightEd)] 


def checkWind2(dir:str, dim:tuple, edges:list, chamber):
    top = dim[0]
    bottom = dim[1]
    left = dim[2]
    right = dim[3]
    botEd = edges[0]
    leftEd = edges[1]
    rightEd = edges[2]

    if dir == "<" and left - 1 >= 0:
        for i in range(len(leftEd)):
            if chamber[leftEd[i, 0], leftEd[i, 1] - 1] != 0:
                break
        else:
            temp = np.copy(chamber[top:bottom + 1, left:right + 1])
            chamber[top:bottom + 1, left:right + 1] = \
                np.where(chamber[top:bottom + 1, left:right + 1] == 1, 0, chamber[top:bottom + 1, left:right + 1])
            chamber[top:bottom + 1, left - 1:right] = \
                np.where(temp == 1, 1, chamber[top:bottom + 1, left - 1:right])

            botEd[:, 1] = botEd[:, 1] - 1
            leftEd[:, 1] = leftEd[:, 1] - 1
            rightEd[:, 1] = rightEd[:, 1] - 1
            left -= 1
            right -= 1

    elif dir == ">" and right + 1 < len(chamber[0]):
        for i in range(len(rightEd)):
            if chamber[rightEd[i, 0], rightEd[i, 1] + 1] != 0:
                break
        else:
            temp = np.copy(chamber[top:bottom + 1, left:right + 1])
            chamber[top:bottom + 1, left:right + 1] = \
                np.where(chamber[top:bottom + 1, left:right + 1] == 1, 0, chamber[top:bottom + 1, left:right + 1])

            chamber[top:bottom + 1, left + 1:right + 2] = \
            np.where(temp == 1, 1, chamber[top:bottom + 1, left + 1:right + 2])

            botEd[:, 1] = botEd[:, 1] + 1
            leftEd[:, 1] = leftEd[:, 1] + 1
            rightEd[:, 1] = rightEd[:, 1] + 1
            left += 1
            right += 1

    return (top, bottom, left, right), [botEd, leftEd, rightEd]

def checkDown2(dim:tuple, edges:list, chamber):
    top = dim[0]
    bottom = dim[1]
    left = dim[2]
    right = dim[3]
    botEd = edges[0]
    leftEd = edges[1]
    rightEd = edges[2]

    if bottom + 1 < len(chamber):

        for i in range(len(botEd)):
            if chamber[botEd[i, 0] + 1, botEd[i, 1]] != 0:
                #it can come to rest
                chamber[top:bottom + 1, left:right + 1] = \
                    np.where(chamber[top:bottom + 1, left:right + 1] == 1, 2, chamber[top:bottom + 1, left:right + 1])

                return 0, 0, False
        else:
            temp = np.copy(chamber[top:bottom + 1, left:right + 1])
            chamber[top:bottom + 1, left:right + 1] = \
                np.where(chamber[top:bottom + 1, left:right + 1] == 1, 0, chamber[top:bottom + 1, left:right + 1])

            chamber[top + 1:bottom + 2, left:right + 1] = \
                np.where(temp == 1, 1, chamber[top + 1:bottom + 2, left:right + 1])

            top += 1
            bottom += 1

            botEd[:, 0] = botEd[:, 0] + 1
            leftEd[:, 0] = leftEd[:, 0] + 1
            rightEd[:, 0] = rightEd[:, 0] + 1


            return (top, bottom, left, right), [botEd, leftEd, rightEd], True
            
    else:
        chamber[top:bottom + 1, left:right + 1] = \
            np.where(chamber[top:bottom + 1, left:right + 1] == 1, 2, chamber[top:bottom + 1, left:right + 1])
        
        return 0, 0, False
          

import matplotlib.pyplot as plt
import copy as copy

chamber = np.zeros((2, 7), np.int8)
chamber[0][0] = -1

shIdx = ["-", "+", "J", "|", "¤"]

starts = {}
for s in shIdx:
    st, di, ed = getStart(s)
    starts[s] = st, di, ed

cycledict = {}

idx = 0
idCheck = True

add = 0
height = 0
turn = 0
checkId = 0
done = False
L = 1000000000000
print(len(winds))
while turn < L:
    print(turn)
    shape = shIdx[turn % 5]
    start, dim, edges = starts[shape]
    start = np.copy(start)
    edges = copy.deepcopy(edges)

    if idCheck:
        cycledict[idx] = np.copy(chamber[:30]), (turn, height, shape)
    else:
        if idx in cycledict:
            
            #Might be faulty comparison but seems to work
            if np.array_equal(cycledict[idx][0], chamber[:30]):
                (oldT, oldH, oldSH) = cycledict[idx][1]
                if oldSH == shape:
                    dheight = height - oldH
                    dt = turn - oldT

                    cyc = (L - turn) // dt
                    add += cyc * dheight
                    turn += cyc * dt
                    assert turn <= L
    
    if chamber[0][0] == -1:
        chamber = start
    else:
        chamber = np.concatenate((start, chamber), axis=0)

    inAir = True
    while inAir:
        dim, edges = checkWind2(winds[idx], dim, edges, chamber)

        dim, edges, inAir = checkDown2(dim, edges, chamber)

        
        idx += 1
        if idx >= len(winds):
            idCheck = False
            idx = 0
    
    top = np.argmax(chamber>0) // 7

    chamber = chamber[top:]
    height = len(chamber)

    turn += 1



print(height + add)









