import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day13", "input.txt")

pair = 0
pairList = [[]]

for line in inputList:
    if line == "":
        pair += 1
        pairList.append([])
    else:
        pairList[pair].append(eval(line))



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
            
idx = 0
sum = 0
for pair in pairList:
    idx += 1
    if compare(pair[0], pair[1]) < 0:
        print(idx)
        sum += idx
    


print(sum)
