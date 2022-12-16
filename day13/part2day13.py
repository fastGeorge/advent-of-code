from quicksort import quicksort

import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day13", "input.txt")

pair = 0
signalList = []

for line in inputList:
    if line != "":
        signalList.append(eval(line))

signalList.append([[2]])
signalList.append([[6]])



def compare(left, right):

    if type(left) == int:
        if type(right) == int:
            return left - right
        else:
            return compare([left], right)
    else:
        if type(right) == int:
            return compare(left, [right])
    
    for l, r in zip(left, right):
        sign = compare(l, r)
        if sign != 0:
            return sign

    return len(left) - len(right)   

quicksort(signalList, 0, len(signalList) - 1, compare)

for i, s in enumerate(signalList):
    print(i + 1)
    print(s)

print((1 + signalList.index([[2]])) * (1 + signalList.index([[6]])))