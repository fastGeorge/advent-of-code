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

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection



fig, ax = plt.subplots()

plt.ion()
plt.show()

for pair in sbPairs:
    s = pair[0]
    b = pair[1]
    plt.scatter(s[0], s[1], c='blue')
    plt.scatter(b[0], b[1], c='red')
    plt.plot([s[0], b[0]], [s[1], b[1]], 'red')
    dist = manDist(s, b)
    for p2 in sbPairs:
        s2 = p2[0]
        b2 = p2[1]
        dist2 = manDist(s2, b2)
        if manDist(s, s2) <= dist + dist2:
            plt.plot([s[0], s2[0]], [s[1], s2[1]], 'black')

    
    patches = []
    p = Polygon([(s[0] - dist, s[1]), (s[0], s[1] + dist), (s[0] + dist, s[1]), (s[0], s[1] - dist)], closed=True)
    patches.append(p)
    pat = PatchCollection(patches, alpha=0.5)
    ax.add_collection(pat)
    fig.canvas.flush_events()
    time.sleep(0.1)
plt.scatter(2557297, 3267339, c='green')
plt.ioff()
plt.show()





