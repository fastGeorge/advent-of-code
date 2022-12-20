import sys, os, time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day15", "input.txt")

import numpy as np

def manDist(s:tuple, b:tuple):
    r = s[0] - b[0]
    c = s[1] - b[1]
    return abs(r) + abs(c)

sbPairs = []
for line in inputList:
    line = line.split(":")
    pair = []
    for l in line:
        comma = l.split(",")
        x = int(comma[0].split("=")[-1])
        y = int(comma[1].split("=")[-1])
        pair.append((x, y))
    sbPairs.append(pair)


import z3 as z

def solveP2(bound):

    dDict = {}
    for pair in sbPairs:
        sens = pair[0]
        beac = pair[1]
        dDict[sens] = manDist(sens, beac)

    print(dDict)
    

    sol = z.Solver()

    x, y = z.Int('x'), z.Int('y')
    sol.add(x >= 0)
    sol.add(x <= bound)
    sol.add(y >= 0)
    sol.add(y <= bound)

    for pair in sbPairs:
        sens = pair[0]
        beac = pair[1]
        curr_dist = z.Abs(sens[0] - x) + z.Abs(sens[1] - y)
        sol.add(curr_dist > dDict[sens])
        sol.add(z.And(x != beac[0], y != beac[1]))
    assert sol.check() == z.sat
    mod = sol.model()
    print(mod)
    return mod[x].as_long(), mod[y].as_long()


x, y = solveP2(4000000)

print(x, y, x * 4000000 + y)



