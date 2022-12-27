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

vString = ""
dists = {}
for valve in valves:
    if valve != "AA" and valves[valve] == 0:
        continue

    dists[valve] = {}
    vString += valve + ","

    for target in valves:
        if target == "AA" or valves[target] == 0 or valve == target:
            continue
        way, n = path(valve, target, tunnels)
        dists[valve][target] =  n


vString = vString[:-1].replace("AA", "00")

cache = {}

def recScore(current, mins, vString:str):

    if (current, mins, vString) in cache:
        return cache[(current, mins, vString)]

    bestScore = 0
    for pos in vString.split(","):
        if pos == "00" or pos == current:
            continue


        n = dists[current][pos]

        reMins = mins - n - 1
        if reMins <= 0:
            continue

        vCopy = vString.replace(pos, "00")
        bestScore = max(bestScore, recScore(pos, reMins, vCopy) + valves[pos] * reMins)

    cache[(current, mins, vString)] = bestScore
    return bestScore


print(recScore("AA", 30, vString))

from itertools import combinations

combList = []
chList = vString.split(",")

for n in range((len(chList) // 2)):
    combList += list(combinations(chList, n + 1))


bestV = 0
iter = 0
for part in combList:
    iter += 1
    if iter % 1000 == 0:
        print(iter)
    elString = ""
    youString = vString
    for v in part:
        elString += v + ","
        youString = youString.replace(v, "00")
    elString = elString[:-1]
    bestV = max(bestV, recScore("AA", 26, elString) + recScore("AA", 26, youString))


print(bestV)



