def getLinesInputFile(day, fileName):
    dir = "C:\\Users\\gusta\\git\\advent-of-code\\" + day +"\\" + fileName
    file = open(dir, "r")
    lines = file.readlines()
    file.close()
    stripped_lines = []
    for l in lines:
        stripped_lines.append(l.strip())
    return stripped_lines
    




