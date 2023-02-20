import sys, os, time, math
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day20", "input.txt")

#Skapa vektor
#Gör kopia
#Håll koll på position


arr = np.ones((len(inputList), 2), np.int64)
#print(arr)

for idx, val in enumerate(inputList):
    arr[idx , 0] = int(val) * 811589153
    arr[idx, 1] = idx


arr_change = arr.copy()




#REALISATION: it only matters where the digit of interest ends up, you only 
# need to know the new index


size = len(arr_change)
for i in range(10):
    for r in arr:
        idx = np.where(arr_change[:,1] == r[1])[0].item()
        move = arr_change[idx, 0]

        to_move = np.copy(arr_change[idx])
        to_move = np.array([to_move])

        #Python uses floored divison for modulus operation -> will always return positive result when denominator is positive
        #What this means is that we get the desired idx straight away from the following line of code.
        #This works since the list is circular (the idea of modular arithmetic applies)
        new_idx = (idx + move) % (size - 1)

        arr_ = 0
        if idx == size - 1:
            arr_ = arr_change[0:idx,:]
        else:
            arr_ = np.concatenate((arr_change[0:idx,:], arr_change[idx + 1:,:]))
            
        arr_change = np.concatenate((arr_[0:new_idx,:], to_move, arr_[new_idx:,:]))



#Find 0
idx = np.where(arr_change[:,0] == 0)[0].item()
print(idx)

#loop round with starting point in 0 until reaching 1000, 2000, and 3000
sum = 0
curr = idx + 1
for i in range(3000):
    if curr > len(arr_change) - 1:
        curr = 0
    if (i + 1) % 1000 == 0:
        sum += arr_change[curr,0]

    curr += 1

print(sum)














