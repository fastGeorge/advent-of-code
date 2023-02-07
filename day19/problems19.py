import sys, os, time, math

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from filereader.filereader import getLinesInputFile
inputList = getLinesInputFile("day19", "input.txt")

blueprints = {}

for line in inputList:
    split = line.split(":")
    digits = [int(i) for i in split[1].split() if i.isdigit()]
    blueprints[int(split[0].split()[-1])] = {
        "ore": (0, [(0, digits[0])]), 
        "clay": (1, [(0, digits[1])]),
        "obs": (2, [(0, digits[2]), (1, digits[3])]),
        "geo": (3, [(0, digits[4]), (2, digits[5])]),
        "max_types": {
            "max_ore": max(digits[0], digits[1], digits[2], digits[4]),
            "max_clay": digits[3],
            "max_obs": digits[5]
        }
    }


    
#inv[0] = ore inv[1] = clay inv[2] = obsidian
inv = [0, 0, 0, 0]

#robots[0] = ore, robots[1] = clay, robots[2] = obs, robots[3] = geode
rob = [1, 0, 0, 0]


def blueScore(inv:list, robots:list, blueprint:dict, mins:int, cache:dict):
    

    key = (inv[0], inv[1], inv[2], inv[3], robots[0], robots[1], robots[2], robots[3], mins)

    if key in cache:
        return cache[key]

    max_score = inv[3] + robots[3] * mins

    for r_type in blueprint:

        if r_type == "max_types":
            continue
        
        idx, r_req = blueprint[r_type]

        if r_type != "geo" and robots[idx] >= blueprint["max_types"]["max_" + r_type]:
            continue

        req_min = 0
        for elem, cost in r_req:
            if robots[elem] == 0:
                break
            
            amt_need = cost - inv[elem]
            rmin_ = math.ceil(amt_need / robots[elem])
            req_min = max(req_min, rmin_)
        else:

            rem_time = mins - req_min - 1
            if rem_time <= 0:
                continue

            inv_ = inv[:]

            for i, val in enumerate(inv_):
                inv_[i] += (req_min + 1) * robots[i]
            
            for elem, cost in r_req:
                inv_[elem] -= cost
            
            rob_ = robots[:]
            rob_[idx] += 1

            for i in range(3):
                s = "max_"
                if i == 0:
                    s += "ore"
                elif i == 1:
                    s += "clay"
                elif i == 2:
                    s += "obs"

                inv_[i] = min(inv_[i], rem_time * blueprint["max_types"][s]) 

            max_score = max(max_score, blueScore(inv_, rob_, blueprint, rem_time, cache))

    
    cache[key] = max_score
    return max_score

mult = 1
for idx in blueprints:
    if idx > 3:
        break
    cache = {}
    mult *= blueScore(inv, rob, blueprints[idx], 32, cache)


print(mult)