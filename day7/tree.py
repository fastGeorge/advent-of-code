
class Node:
    def __init__(self, data, parent):
        self.data = data
        self.children = []
        self.parent = parent

    def setData(self, data):
        self.data = data

    def addChild(self, child):
        self.children.append(child)

    def __str__(self):
        return str(self.data)

class Tree:

    def __init__(self, root:Node):
        self.root = root

def readCDLS(contains:list, node:Node):
    nodeList = []
    for item in contains:
        n = Node()
        n.setData(item)
        nodeList.append(n)
    node.setChildren(nodeList)


    

