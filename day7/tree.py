
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




    

