import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
from collections import deque

inputList = getLinesInputFile("day6", "input.txt")

marker = list()
idx = 0
for i in inputList[0]:
    marker.append(ord(i))
    idx += 1
    chIdx = 0
    for ch in marker[:len(marker) -1]:
        if(ch == marker[-1]):
            marker = marker[chIdx + 1:]
        chIdx += 1
    if len(marker) == 14:
        print(idx)
        break




     

    
