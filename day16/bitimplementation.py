import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day16", "input.txt")

valves = {}
tunnels = {}
for line in inputList:
    flow_tun = line.split(";")
    valve = flow_tun[0].split()[1]
    flowRate = int(flow_tun[0].split("=")[-1])
    step = flow_tun[1].split(",")
    tStep = []
    for i in step:
        tStep.append(i.split()[-1])
    valves[valve] = flowRate
    tunnels[valve] = tStep
    
import heapq
from collections import deque



def reconstructPath(cameFrom:dict, current):
    path = deque()
    path.append(current)
    while current in cameFrom:
        current = cameFrom[current]
        path.appendleft(current)
    return path

def path(start:str, goal:str, map:dict):

    pq = []
    heapq.heappush(pq, (0, start))

    cameFrom = dict()

    gScore = dict()
    for idx in map:
        gScore[idx] = sys.maxsize
    gScore[start] = 0

    while len(pq) > 0:
        
        current = heapq.heappop(pq)[1]
        if current == goal:
            return reconstructPath(cameFrom, current), gScore[current]
        
        for neighbor in map[current]:
            
            tentative_G = gScore[current] + 1
            if tentative_G < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_G
                heapq.heappush(pq, (gScore[neighbor], neighbor))
    return None

valveCond = {}
vString = ""
dists = {}
for valve in valves:
    if valve != "AA" and valves[valve] == 0:
        continue

    dists[valve] = {}
    valveCond[valve] = 1
    vString += valve + ","

    for target in valves:
        if target == "AA" or valves[target] == 0 or valve == target:
            continue
        way, n = path(valve, target, tunnels)
        dists[valve][target] =  n

valveCond["AA"] = 0
vString = vString[:-1]
vString = vString.replace("AA", "00")

openValve = {}

for i, valve in enumerate(dists):
    openValve[valve] = i


cache = {}

    
def recScore(current, mins, bitmask):

    if (current, mins, bitmask) in cache:
        return cache[(current, mins, bitmask)]

    bestScore = 0
    for pos in dists[current]:

        #Shifts the 1 openValve[pos] steps to the left adding zeros after
        bit = 1 << openValve[pos]

        #if the 1 in bit alligns with a 1 in bitmask a nonzero result is given, 
        # signalling that the valve is already open and should be skipped
        if bit & bitmask != 0:
            continue

        n = dists[current][pos]

        reMins = mins - n - 1
        if reMins <= 0:
            continue
        
        #Here it is registered in bitmask that the current valve has been opened
        #  by adding a one to the bitmask at the location indicated in openValve[pos]
        newBitmask = bit | bitmask
        bestScore = max(bestScore, recScore(pos, reMins, newBitmask) + valves[pos] * reMins)

    cache[(current, mins, bitmask)] = bestScore
    return bestScore

#Bitmask starts at 0 to indicate that all valves are closed
print(recScore("AA", 30, 0))