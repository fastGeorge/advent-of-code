import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day11", "input.txt")


class Monkey:

    def __init__(self, items:list, operation:str, cond:int, trueM:int, falseM:int):
        self.items = items
        self.operation = operation
        self.cond = cond
        self.trueM = trueM
        self.falseM = falseM
        self.inspected = 0

    def turn(self, monkeyList:list, mod:int):
        op = self.operation
        for item in self.items:
            self.inspected += 1
            if op.__contains__("old * old"):
                item = item * item
            else:
                opSplit = op.split()
                nbr = int(op[-1])
                if opSplit[1] == "+":
                    item += nbr
                elif opSplit[1] == "*":
                    item *= nbr
            final = item % mod
            if final % self.cond == 0:
                monkeyList[self.trueM].items.append(final)
            else:
                monkeyList[self.falseM].items.append(final)
        self.items = []

monkeyList = []
i = 0
while i < len(inputList):
    split = inputList[i].split()
    if split[0] == "Monkey":
        items = [] 
        operation = None
        cond = None
        trueM = None
        falseM = None
        while i < len(inputList) and inputList[i] != "":
            l = inputList[i]
            if l.__contains__("Starting items"):
                l = l.split(":")
                nbrs = [int(k) for k in l[1].split(",") if k.strip().isdigit()]
                for item in nbrs:
                    items.append(item)
            elif l.__contains__("Operation"):
                l = l.split("=")
                operation = l[1]
            elif l.__contains__("Test"):
                l = l.split()
                cond = int(l[-1])
            elif l.__contains__("If true"):
                l = l.split()
                trueM = int(l[-1])
            elif l.__contains__("If false"):
                l = l.split()
                falseM = int(l[-1])
            i += 1
        monkeyList.append(Monkey(items, operation, cond, trueM, falseM))
    i += 1

mod = 1
for m in monkeyList:
    mod *= m.cond
print(mod)
round = 0
while round < 10000:
    for m in monkeyList:
        m.turn(monkeyList, mod)
    round += 1


nbr1 = 0
nbr2 = 0
for m in monkeyList:
    nbr = m.inspected
    if nbr > nbr1:
        nbr2 = nbr1
        nbr1 = nbr
    elif nbr > nbr2:
        nbr2 = nbr

print(nbr1, " ", nbr2)
print(nbr1*nbr2)