import sys
sys.path.append("../advent-of-code")

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day10", "input.txt")

cycle = 0
x = 1
twentList = []
for line in inputList:
    split = line.split()
    if split[0] == "noop":
        cycle += 1
        if (cycle - 20) % 40 == 0:
            twentList.append(cycle * x)
    elif split[0] == "addx":
        cycle += 1
        if (cycle - 20) % 40 == 0:
            twentList.append(cycle * x)
        cycle += 1
        if (cycle - 20) % 40 == 0:
            twentList.append(cycle * x)
        x += int(split[1])

print(twentList)

print(sum(twentList))
