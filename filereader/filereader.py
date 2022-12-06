def getLinesInputFile(day, fileName):
    dir = "C:\\Users\\gusta\\git\\advent-of-code\\" + day +"\\" + fileName
    file = open(dir, "r")
    lines = file.readlines()
    file.close()
    return lines
    




