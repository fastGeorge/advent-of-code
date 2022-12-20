import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day16", "input.txt")

valves = {}
for line in inputList:
    flow_tun = line.split(";")
    valve = flow_tun[0].split()[1]
    flowRate = int(flow_tun[0].split("=")[-1])
    step = flow_tun[1].split(",")
    tunnels = []
    for i in step:
        tunnels.append(i.split()[-1])
    valves[valve] = (flowRate, tunnels)

from day13.quicksort import *

def valveSort(valves:dict):
    def compare(el1, el2):
        return el1[1] - el2[1]

    sortList = []
    for s in valves:
        sortList.append((s, valves[s][0]))
    quicksort(sortList, 0, len(sortList) - 1, compare)
    return sortList
    
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
        
        for neighbor in map[current][1]:
            
            tentative_G = gScore[current] + 1
            if tentative_G < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_G
                heapq.heappush(pq, (gScore[neighbor], neighbor))
    return None

# sortList = valveSort(valves)
# way, dist = path("AA", "AA", valves)
# print(way)
# onlyZeros = False
# mins = 30
# flowComb = 0
# flowRes = 0
# current = "AA"
# while not onlyZeros and mins > 0:
    
#     bestOp = None
#     bestPath = None
#     bestScore = 0
#     minDiff = 0
#     for pos in reversed(sortList):
#         if pos[1] == 0:
#             break

#         way, n = path(current, pos[0], valves)
#         print(pos)
#         print((mins - (n + 1)) * pos[1])
#         if (mins - (n + 1)) * pos[1] > bestScore:
#             bestScore = (mins - (n + 1)) * pos[1]
#             bestOp = pos[0]
#             bestPath = way
#             minDiff = (n + 1)

#     flowRes += flowComb * minDiff
#     current = bestOp
#     print(bestPath)
#     flowComb += valves[current][0]
#     valves[current] = (0, valves[current][1])
#     sortList = valveSort(valves)
#     onlyZeros =  sortList[-1][1] == 0
#     mins -= minDiff

# flowRes += flowComb * mins
# print(flowRes)
    
def recScore(copyValves:dict, current, mins, flowComb, flowRes):
    #print(flowRes)
    sortList = valveSort(copyValves)
    if sortList[-1][1] == 0 or mins == 0:
        return flowRes + (mins * flowComb)
    bestScore = 0

    for pos in reversed(sortList):
        if pos[1] == 0:
            return bestScore
        
        way, n = path(current, pos[0], copyValves)

        
        copy = copyValves.copy()
        copy[pos[0]] = (0, copyValves[pos[0]][1])

        score = 0
        if mins - (n + 1) < 0:
            score = flowRes + (mins * flowComb)
        else:
            score = recScore(copy, pos[0], mins - (n + 1), flowComb + copyValves[pos[0]][0], flowRes + (flowComb * (n + 1)))
            
        if score > bestScore:
            bestScore = score
            #print(way)


print(recScore(valves.copy(), "AA", 30, 0, 0))


