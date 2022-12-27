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

print(winds)

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
        #print(arr)
        rowBot = np.argmax(arr>0)
        #print(rowBot)
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



#plt.ion()

fig, ax = plt.subplots()

chamber = np.zeros((2, 7), np.int8)
chamber[0][0] = -1

plot = plt.imshow(chamber, cmap='tab20', aspect="equal", vmin=0, vmax=2)
#plt.show()

t0 = time.time()

height = 0
turns = 0
shIdx = ["-", "+", "J", "|", "¤"]

starts = {}
for s in shIdx:
    st, di, ed = getStart(s)
    starts[s] = st, di, ed


idx = 0
while turns < 2022:
    shape = shIdx[turns % 5]
    start, dim, edges = getStart(shape)
    
    if chamber[0][0] == -1:
        chamber = start
    else:
        chamber = np.concatenate((start, chamber), axis=0)
    inAir = True
    while inAir:
        #time.sleep(0.2)

        dim, edges = checkWind2(winds[idx], dim, edges, chamber)

        # plot.set_extent([0, 6, 0, len(chamber)])
        # plot.set_data(chamber)


        # fig.canvas.flush_events()

        dim, edges, inAir = checkDown2(dim, edges, chamber)


        # plot.set_data(chamber)
        # fig.canvas.flush_events()

        
        idx += 1
        if idx >= len(winds):
            idx = 0
    
    top = np.argmax(chamber>0) // 7

    chamber = chamber[top:]

    botVal = 0
    for i in range(7):
        c = chamber[:, i]
        b = np.argmax(c)
        if b != 0 or c[0] == 2:
            botVal = max(b, botVal)
        else:
            break
    else:
        height += len(chamber[botVal + 1:])
        chamber = chamber[:botVal + 1]

    turns += 1

#print(chamber)
print(height + len(chamber))
print(time.time() - t0)
#plt.ioff()
#plt.show()









