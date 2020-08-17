import data
import itertools

def notForbidden(names, FORBIDDEN):
    for name in names:
        if name in FORBIDDEN:
            return False
    return True

def wanted(names, WANTED):
    if (all(x in names for x in WANTED)):
        return True
    else:
        return False
def matchFixing(present, TEAM_STANDINGS, PAST_SEASON):
    for key, value in TEAM_STANDINGS.items():
        TEAM_STANDINGS.update({key: present*value + (1-present)*PAST_SEASON.get(key)})

def totalUpset(TEAM_STANDINGS, NA, PAST_SEASON):
    upsetNA = 0
    upsetEU = 0
    for key in TEAM_STANDINGS.keys():
        if key in NA:
            upsetNA += abs(TEAM_STANDINGS.get(key) - PAST_SEASON.get(key))
        else:
            upsetEU += abs(TEAM_STANDINGS.get(key) - PAST_SEASON.get(key))
    print(upsetNA, upsetEU)

def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num

def lookAtPast():

    bestTeams = []

    for present in [1, 0.9, 0.8, 0.7, 0.6, 0.5]:

        data.updateStandings()
        matchFixing(present)

        TOP = data.parseRole("top")
        JNG = data.parseRole("jng")
        MID = data.parseRole("mid")
        ADC = data.parseRole("adc")
        SUPP = data.parseRole("supp")
        TEAMS = data.parseTeam("teams")
        ROLES = [TOP, JNG, MID, ADC, SUPP, TEAMS]

        bestInRole = []

        for role in ROLES:
            sortedArray = sorted(role, key=lambda x: x[3])
            bestInRole.append(sortedArray[:12])

        combos = []

        for toplaner in bestInRole[0]:
            for jungler in bestInRole[1]:
                for midlaner in bestInRole[2]:
                    for adcarry in bestInRole[3]:
                        for support in bestInRole[4]:
                            for squad in bestInRole[5]:
                                totalPoints = toplaner[2] + jungler[2] + midlaner[2] + adcarry[2] + support[2] + squad[2]
                                mid_adc_team = adcarry[2] * 1.5 + midlaner[2] + squad[2]
                                totalPrice = toplaner[1] + jungler[1] + midlaner[1] + adcarry[1] + support[1] + squad[1]
                                if totalPrice < 1500 and "WildTurtle" not in adcarry[0] and "Huni" not in toplaner[0] and "Perkz" not in adcarry[0] and "Meteos" not in jungler[0] and "Stunt" not in support[0] and "Eika" not in midlaner[0]:
                                    combos.append([[toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]],totalPoints, mid_adc_team / totalPoints])

        bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)
        #print(bestCombos[:5])
        bestTeams.append(bestCombos[0])
        bestTeams.append(bestCombos[1])
        bestTeams.append(bestCombos[2])
    bestTeams = sorted(combos, key=lambda x: x[1], reverse=True)
    print(bestTeams[:5])

def mostRobust(TEAM_STANDINGS):

    bagNA = ["TSM", "100", "GG", "TL", "CLG"]
    bagEU = ["RGE", "MSF", "SK", "VIT"]

    pointsEU = [6, 5, 4, 3]
    pointsNA = [7, 6, 5, 4, 3]

    standingsNA = {}
    standingsEU = {}

    standingsNA["C9"]=10
    standingsNA["FLY"]=9
    standingsNA["EG"]=9
    standingsNA["IMT"]=2
    standingsNA["DIG"]=2

    standingsEU["G2"]=10
    standingsEU["FNC"]=9
    standingsEU["OG"]=9
    standingsEU["MAD"]=9
    standingsEU["XL"]=2
    standingsEU["S04"]=1

    cycle = 0
    bestSimulations = []

    for permutationEU in itertools.permutations(pointsEU):
        for permutationNA in itertools.permutations(pointsNA):
            print("FUTURE NUMBER: " + str(cycle))
            for j in range(0, 4):
                standingsEU[bagEU[j]]=permutationEU[j]
            for j in range(0, 5):
                standingsNA[bagNA[j]]=permutationNA[j]

            TEAM_STANDINGS.update(standingsEU)
            TEAM_STANDINGS.update(standingsNA)



            TOP = data.parseRole("top")
            JNG = data.parseRole("jng")
            MID = data.parseRole("mid")
            ADC = data.parseRole("adc")
            SUPP = data.parseRole("supp")
            TEAMS = data.parseTeam("teams")
            ROLES = [TOP, JNG, MID, ADC, SUPP, TEAMS]

            bestInRole = []

            for role in ROLES:
                sortedArray = sorted(role, key=lambda x: x[3])
                bestInRole.append(sortedArray[:10])

            combos = []

            for toplaner in bestInRole[0]:
                for jungler in bestInRole[1]:
                    for midlaner in bestInRole[2]:
                        for adcarry in bestInRole[3]:
                            for support in bestInRole[4]:
                                for squad in bestInRole[5]:
                                    totalPoints = toplaner[2] + jungler[2] + midlaner[2] + adcarry[2] + support[2] + squad[2]
                                    totalPrice = toplaner[1] + jungler[1] + midlaner[1] + adcarry[1] + support[1] + squad[1]
                                    if totalPrice < 1500 and "WildTurtle" not in adcarry[0]:
                                        combos.append([[toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]], totalPoints])

            bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)
            #print(bestCombos[:1])

            bestSimulations.append(bestCombos[0][0])
            cycle += 1

    print(most_frequent(bestSimulations))

def mostLikely(TEAM_STANDINGS):

    standingsNA = {}
    standingsEU = {}

    standingsNA["C9"] = 10
    standingsNA["FLY"] = 7.5
    standingsNA["EG"] = 8
    standingsNA["TL"] = 7
    standingsNA["TSM"] = 7
    standingsNA["CLG"] = 5
    standingsNA["100"] = 4
    standingsNA["GG"] = 3
    standingsNA["IMT"] = 3
    standingsNA["DIG"] = 2

    standingsEU["G2"] = 9
    standingsEU["FNC"] = 8
    standingsEU["OG"] = 8
    standingsEU["MAD"] = 9
    standingsEU["RGE"] = 8
    standingsEU["SK"] = 6
    standingsEU["MSF"] = 6
    standingsEU["VIT"] = 5
    standingsEU["XL"] = 3
    standingsEU["S04"] = 2

    TEAM_STANDINGS.update(standingsEU)
    TEAM_STANDINGS.update(standingsNA)

    TOP = data.parseRole("top")
    JNG = data.parseRole("jng")
    MID = data.parseRole("mid")
    ADC = data.parseRole("adc")
    SUPP = data.parseRole("supp")
    TEAMS = data.parseTeam("teams")
    ROLES = [TOP, JNG, MID, ADC, SUPP, TEAMS]

    bestInRole = []

    for role in ROLES:
        sortedArray = sorted(role, key=lambda x: x[3])
        print(sortedArray)
        bestInRole.append(sortedArray[:15])

    combos = []

    for toplaner in bestInRole[0]:
        for jungler in bestInRole[1]:
            for midlaner in bestInRole[2]:
                for adcarry in bestInRole[3]:
                    for support in bestInRole[4]:
                        for squad in bestInRole[5]:
                            totalPoints = toplaner[2] + jungler[2] + midlaner[2] + adcarry[2]*1.5 + support[2] + squad[2]
                            mid_adc_team = adcarry[2]*1.5+midlaner[2]+squad[2]
                            totalPrice = toplaner[1] + jungler[1] + midlaner[1] + adcarry[1] + support[1] + squad[1]
                            if totalPrice < 1500 and "WildTurtle" not in adcarry[0] and "Huni" not in toplaner[0] and "Perkz" not in adcarry[0] and "Meteos" not in jungler[0] and "Stunt" not in support[0] :
                                combos.append([[toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]],
                                               totalPoints, mid_adc_team/totalPoints])

    bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)[:30]
    toDisplay = sorted(bestCombos, key=lambda x: x[2])
    print(toDisplay)

    toDisplay = sorted(bestCombos, key=lambda x: x[1])
    print(toDisplay)

def mostImportantFirst(lecStandings, lcsStandings, TEAM_STANDINGS, TEAM_NAMES, week, ROLE_MODIFIERS, DATA, FORBIDDEN, WANTED):

    data.updateStandings(lecStandings, lcsStandings, TEAM_STANDINGS, TEAM_NAMES)

    TOP = data.parseRole("top", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    JNG = data.parseRole("jng", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    MID = data.parseRole("mid", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    ADC = data.parseRole("adc", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    SUPP = data.parseRole("supp", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    TEAMS = data.parseTeam("teams", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    ROLES = [TOP, JNG, MID, ADC, SUPP, TEAMS]

    bestInRole = []

    for role in ROLES:
        sortedArray = sorted(role, key=lambda x: x[3], reverse=True)
        bestInRole.append(sortedArray[:12])
        print(sortedArray)

    combos = []

    for toplaner in bestInRole[0]:
        for jungler in bestInRole[1]:
            for midlaner in bestInRole[2]:
                for adcarry in bestInRole[3]:
                    for support in bestInRole[4]:
                        for squad in bestInRole[5]:
                            mostImportant = midlaner[2] + adcarry[2] + squad[2]
                            totalPoints = toplaner[2] + jungler[2] + midlaner[2] + adcarry[2] + support[2] + squad[2]
                            totalPrice = toplaner[1] + jungler[1] + midlaner[1] + adcarry[1] + support[1] + squad[1]
                            totalSafety = toplaner[4] + jungler[4] + midlaner[4] + adcarry[4] + support[4] + squad[4]
                            imbalance = mostImportant / totalPoints
                            names = [toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]]
                            if totalPrice < 1500 and notForbidden(names, FORBIDDEN):
                                combos.append([names, totalPoints, totalSafety, mostImportant, totalPrice, imbalance])


    print("Best combos overall")
    bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)
    print(bestCombos[:10])
    print("----")
    print("Safest combos")
    safestCombos = sorted(combos, key=lambda x: x[2], reverse=True)
    safestCombos = safestCombos[:15]
    safestCombos = sorted(safestCombos, key=lambda x: x[1], reverse=True)
    print(safestCombos[:10])
    print("----")
    print("Best combos with best relevant roles")
    mostImportantCombos = sorted(combos, key=lambda x: x[3], reverse=True)
    print(mostImportantCombos[:10])
    print("----")
    print("Most balanced combos")
    mostBalancedCombos = sorted(combos, key=lambda x: x[5], reverse=False)
    print(mostBalancedCombos[:10])

def mostImportantFirst2(lecStandings, lcsStandings, TEAM_STANDINGS, TEAM_NAMES, week, ROLE_MODIFIERS, DATA, FORBIDDEN, WANTED):

    data.updateStandings(lecStandings, lcsStandings, TEAM_STANDINGS, TEAM_NAMES)

    TOP = data.parseRole2("top", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    JNG = data.parseRole2("jng", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    MID = data.parseRole2("mid", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    ADC = data.parseRole2("adc", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    SUPP = data.parseRole2("supp", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    TEAMS = data.parseTeam2("teams", week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA)
    ROLES = [TOP, JNG, MID, ADC, SUPP, TEAMS]

    bestInRole = []

    for role in ROLES:
        sortedArray = sorted(role, key=lambda x: x[3], reverse=True)
        bestInRole.append(sortedArray[:12])
        print(sortedArray)

    combos = []

    for toplaner in bestInRole[0]:
        for jungler in bestInRole[1]:
            for midlaner in bestInRole[2]:
                for adcarry in bestInRole[3]:
                    for support in bestInRole[4]:
                        for squad in bestInRole[5]:
                            mostImportant = midlaner[2] + adcarry[2] + squad[2]
                            totalPoints = toplaner[2] + jungler[2] + midlaner[2] + adcarry[2] + support[2] + squad[2]
                            totalPrice = toplaner[1] + jungler[1] + midlaner[1] + adcarry[1] + support[1] + squad[1]
                            totalSafety = toplaner[4] + jungler[4] + midlaner[4] + adcarry[4] + support[4] + squad[4]
                            imbalance = mostImportant / totalPoints
                            names = [toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]]
                            if totalPrice < 1500 and notForbidden(names, FORBIDDEN):
                                combos.append([names, totalPoints, totalSafety, mostImportant, totalPrice, imbalance])


    print("Best combos overall")
    bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)
    print(bestCombos[:10])
    print("----")
    print("Safest combos")
    safestCombos = sorted(combos, key=lambda x: x[2], reverse=True)
    safestCombos = safestCombos[:15]
    safestCombos = sorted(safestCombos, key=lambda x: x[1], reverse=True)
    print(safestCombos[:10])
    print("----")
    print("Best combos with best relevant roles")
    mostImportantCombos = sorted(combos, key=lambda x: x[3], reverse=True)
    print(mostImportantCombos[:10])
    print("----")
    print("Most balanced combos")
    mostBalancedCombos = sorted(combos, key=lambda x: x[5], reverse=False)
    print(mostBalancedCombos[:10])