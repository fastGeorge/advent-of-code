import sys
from tree import *
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile

inputList = getLinesInputFile("day7", "input.txt")

dirList = []
dirList

level = 0
root = Node(None, None)
root.addChild(Node("/", root))

currentNode = root

for line in inputList:
    line = line.strip()
    split = line.split()
    if split[0] == "$":
        if split[1] == "cd":
            if split[2] == "/":
                    currentNode = root.children[0]
            elif split[2] != "..":
                for n in currentNode.children:
                    if n.data == split[2]:
                        currentNode = n
                        break
            else:
                currentNode = currentNode.parent
    else:
        if split[0] == "dir":
            currentNode.addChild(Node(split[1], currentNode))
        else:
            currentNode.addChild(Node(int(split[0]), currentNode))
    

def getSumDir(root:Node):
    
    sum = 0
    for n in root.children:
        
        if len(n.children) == 0:
            sum += n.data
            #print(n.data)
        else:
            res = getSumDir(n)
            
            dirList.append([n.data, res])
            sum += res
    
    return sum


totSum = getSumDir(root)

spaceLeft = 70000000 - totSum

spaceNeeded = 30000000 - spaceLeft

print(spaceNeeded)

smallestDir = sys.maxsize
for i in dirList:
    if(i[1] < smallestDir and i[1] >= spaceNeeded):
        smallestDir = i[1]

print(smallestDir)








