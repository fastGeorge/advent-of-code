import sys, os, time, math
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day21", "input.txt")

monkeys = {}
for line in inputList:
    parts = line.split(": ")
    monkeys[parts[0]] = parts[1]



def getRoot(monkeys:dict, monkey:str):

    if monkey == "humn":
        return -1
    
    op = monkeys[monkey]

    if op.isdigit():
        return int(op)
    else:
        op_p = op.split()
        #monkey operation monkey
        mon_1 = getRoot(monkeys, op_p[0])
        mon_2 = getRoot(monkeys, op_p[2])
        if mon_1 == -1 or mon_2 == -1:
            return -1
        elif op_p[1] == "+":
            return mon_1 + mon_2
        elif op_p[1] == "-":
            return mon_1 - mon_2
        elif op_p[1] == "*":
            return mon_1 * mon_2
        elif op_p[1] == "/":
            return mon_1 / mon_2
    

# Part one, gives wrong result since method was modified for part 2
print(getRoot(monkeys, "root"))

# Part 2

root_comp = monkeys["root"].split()

val1 = getRoot(monkeys, root_comp[0])
val2 = getRoot(monkeys, root_comp[2])

print(val1, val2)

eq_val = max(val1, val2)

if val1 > val2:
    humn_path_mon = root_comp[2]
else:
    eq_val = val2
    humn_path_mon = root_comp[0]


from tree import Node

def getNode(monkeys:dict, monkey:str):
    
    if monkey == "humn":
        return monkey
    
    op = monkeys[monkey]

    if op.isdigit():
        return int(op)
    else:
        op_p = op.split()
        node_op = op_p[1]
        children = []
        val1 = getRoot(monkeys, op_p[0])
        if val1 != -1:
            children.append(val1)
        else:
            children.append(getNode(monkeys, op_p[0]))

        val2 = getRoot(monkeys, op_p[2])
        if val2 != -1:
            children.append(val2)
        else:
            children.append(getNode(monkeys, op_p[2]))
        

        return Node(node_op, children)



operationTree = getNode(monkeys, humn_path_mon)

# start at wanted value
# check both sides
# The side that is Node is saved as path
# The other side is handled in terms of operation
# a new value is tested

path = operationTree

x = eq_val

humn_found = False

while not humn_found:
    ch = path.children
    op = path.op
    x_is_left = True
    val = 0
    if ch[0] == "humn":
        val = ch[1]
        humn_found = True
    elif ch[1] == "humn":
        val = ch[0]
        humn_found = True
        x_is_left = False
    elif isinstance(ch[0], Node):
        path = ch[0]
        val = ch[1]
    elif isinstance(ch[1], Node):
        path = ch[1]
        val = ch[0]
        x_is_left = False
    else:
        print("something went wrong!!!!!!!!!!")


    if op == "+":
        x -= val
    elif op == "-":
        if x_is_left:
            x += val
        else:
            x = val - x
    elif op == "*":
        x /= val
    elif op == "/":
        if x_is_left:
            x *= val
        else:
            x = val / x

print(x)