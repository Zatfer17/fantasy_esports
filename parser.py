import pandas as pd
import requests
from bs4 import BeautifulSoup
import itertools

lecStandings = "https://lol.gamepedia.com/LEC/2020_Season/Summer_Season"
lcsStandings = "https://lol.gamepedia.com/LCS/2020_Season/Summer_Season"

#lecStandings = "https://web.archive.org/web/20200618203129/https://lol.gamepedia.com/LEC/2020_Season/Summer_Season"
#lcsStandings = "https://web.archive.org/web/20200619002145/https://lol.gamepedia.com/LCS/2020_Season/Summer_Season"

week = "4th"

TEAM_STANDINGS = {}
TEAM_NAMES = {
    "Dignitas": "DIG",
    "Immortals": "IMT",
    "Evil Geniuses": "EG",
    "SK Gaming": "SK",
    "FC Schalke 04": "S04",
    "100 Thieves": "100",
    "MAD Lions": "MAD",
    "G2 Esports": "G2",
    "Cloud9": "C9",
    "Team SoloMid": "TSM",
    "Fnatic": "FNC",
    "Golden Guardians": "GG",
    "Origen": "OG",
    "Team Liquid": "TL",
    "Team Vitality": "VIT",
    "Counter Logic Gaming": "CLG",
    "Rogue": "RGE",
    "Misfits Gaming": "MSF",
    "FlyQuest": "FLY",
    "Excel Esports": "XL"
}

PAST_SEASON = {
    "C9":10,
    "FLY":9,
    "EG":8,
    "TSM":7,
    "100":6,
    "GG":5,
    "DIG":4,
    "IMT":3,
    "TL":2,
    "CLG":1,
    "G2":10,
    "FNC":9,
    "MAD":8,
    "OG":8,
    "RGE":7,
    "MSF":6,
    "XL":5,
    "S04":4,
    "SK":3,
    "VIT":2
}

NA = ["C9","FLY","EG","TSM","100","GG","DIG","IMT","TL","CLG"]
EU = ["G2","FNC","MAD","OG","RGE","MSF","XL","S04","SK","VIT"]

DATA = []

ROLE_MODIFIERS = {
    "top": 0.8,
    "jng": 0.8,
    "mid": 0.8,
    "adc": 0.8,
    "supp": 0.8,
    "teams": 0.75
}


def parseRole(role):
    table = []
    numLines =  sum(1 for line in open("data/"+week+"_week/"+role+".txt", "r")) - 1
    file = open("data/"+week+"_week/"+role+".txt", "r")
    file.seek(1)
    for i in range(0, int(numLines/12)):
        row = [next(file) for x in range(12)]
        role = role.upper()
        name = row[1].replace("\n", "")
        team = row[3].replace("\n", "")
        salary = float(row[5].replace("\n", "").replace("$", "").replace(".000", ""))
        points = float(row[6].replace("\n", "").replace("-", "0"))
        enemy1 = str(row[8].replace("\n", ""))
        enemy2 = str(row[10].replace("\n", ""))

        ownRank = TEAM_STANDINGS.get(team)
        enemy1Rank = TEAM_STANDINGS.get(enemy1)
        enemy2Rank = TEAM_STANDINGS.get(enemy2)

        pts1 = points * (1+(ownRank-enemy1Rank)/10) * ROLE_MODIFIERS.get(role.lower())
        pts2 = points * (1+(ownRank-enemy2Rank)/10) * ROLE_MODIFIERS.get(role.lower())

        totalPts = pts1 + pts2
        if totalPts != 0:
            valueForMoney = salary/totalPts
        else:
            valueForMoney = 100

        DATA.append([role, name, team, salary, points, enemy1, pts1, enemy2, pts2, totalPts, valueForMoney])
        table.append([name, salary, totalPts, valueForMoney])
    return table

def parseTeam(role):
    table = []
    numLines =  sum(1 for line in open("data/"+week+"_week/"+role+".txt", "r")) - 1
    file = open("data/"+week+"_week/"+role+".txt", "r")
    file.seek(1)
    for i in range(0, int(numLines/12)):
        row = [next(file) for x in range(12)]
        role = role.upper()
        name = row[1].replace("\n", "")
        team = row[3].replace("\n", "")
        salary = float(row[4].replace("\n", "").replace("$", "").replace(".000", ""))
        points = float(row[5].replace("\n", "").replace("-", "0"))
        enemy1 = str(row[8].replace("\n", ""))
        enemy2 = str(row[10].replace("\n", ""))

        ownRank = TEAM_STANDINGS.get(name)
        enemy1Rank = TEAM_STANDINGS.get(enemy1)
        enemy2Rank = TEAM_STANDINGS.get(enemy2)

        pts1 = points * (1 + (ownRank - enemy1Rank) / 10) * ROLE_MODIFIERS.get(role.lower())
        pts2 = points * (1 + (ownRank - enemy2Rank) / 10) * ROLE_MODIFIERS.get(role.lower())

        totalPts = pts1 + pts2
        if totalPts != 0:
            valueForMoney = salary / totalPts
        else:
            valueForMoney = 100

        DATA.append([role, name, team, salary, points, enemy1, pts1, enemy2, pts2, totalPts, valueForMoney])
        table.append([name, salary, totalPts, valueForMoney])
    return table

def parseData(needUpdate=False):
    if needUpdate:
        updateStandings()

        TOP = parseRole("top")
        JNG = parseRole("jng")
        MID = parseRole("mid")
        ADC = parseRole("adc")
        SUPP = parseRole("supp")
        TEAMS = parseTeam("teams")
        ROLES = [TOP, JNG, MID, ADC, SUPP, TEAMS]

    df = pd.DataFrame(DATA)
    df.to_excel(excel_writer=week + "_week.xlsx")

def updateStandings():
    lec = requests.get(lecStandings).content
    lcs = requests.get(lcsStandings).content

    soup = BeautifulSoup(lec, "html.parser")
    rows = soup.findAll("div", {"class": "standings-outer-div"})
    teamsContainer = rows.pop()
    teams = teamsContainer.contents[0].contents[0].contents[0]
    for i in range(2,12):
        team = teams.contents[i]
        name = team.contents[1].contents[0].contents[1].text
        position = int(team.contents[0].text)
        TEAM_STANDINGS[TEAM_NAMES.get(name)] = (11 - position)

    soup = BeautifulSoup(lcs, "html.parser")
    rows = soup.findAll("div", {"class": "standings-outer-div"})
    teamsContainer = rows.pop()
    teams = teamsContainer.contents[0].contents[0].contents[0]
    for i in range(2, 12):
        team = teams.contents[i]
        name = team.contents[1].contents[0].contents[1].text
        position = int(team.contents[0].text)
        TEAM_STANDINGS[TEAM_NAMES.get(name)] = (11 - position)

def matchFixing(present):
    for key, value in TEAM_STANDINGS.items():
        TEAM_STANDINGS.update({key: present*value + (1-present)*PAST_SEASON.get(key)})

def totalUpset():
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
    bestSimulations = []
    for elem in [0.8, 0.7, 0.6, 0.5, 0.4]:

        print("PRESENT VALUE: " + str(elem))

        updateStandings()
        matchFixing(elem)

        TOP = parseRole("top")
        JNG = parseRole("jng")
        MID = parseRole("mid")
        ADC = parseRole("adc")
        SUPP = parseRole("supp")
        TEAMS = parseTeam("teams")
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
                                totalPoints = toplaner[2] + jungler[2] + midlaner[2] + adcarry[2] + support[2] + squad[
                                    2]
                                totalPrice = toplaner[1] + jungler[1] + midlaner[1] + adcarry[1] + support[1] + squad[1]
                                if totalPrice < 1500 and "WildTurtle" not in adcarry[0] and "Huni" not in toplaner[0]:
                                    combos.append(
                                        [[toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]],
                                         totalPoints])

        bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)
        #print(bestCombos[:6])

        bestSimulations.append(bestCombos[0][0])
        bestSimulations.append(bestCombos[1][0])
        bestSimulations.append(bestCombos[2][0])

    print(most_frequent(bestSimulations))

def mostRobust():

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



            TOP = parseRole("top")
            JNG = parseRole("jng")
            MID = parseRole("mid")
            ADC = parseRole("adc")
            SUPP = parseRole("supp")
            TEAMS = parseTeam("teams")
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

def mostLikely():

    standingsNA = {}
    standingsEU = {}

    standingsNA["C9"] = 10
    standingsNA["FLY"] = 8
    standingsNA["EG"] = 8
    standingsNA["TL"] = 7
    standingsNA["TSM"] = 6
    standingsNA["100"] = 5
    standingsNA["CLG"] = 5
    standingsNA["GG"] = 3
    standingsNA["IMT"] = 3
    standingsNA["DIG"] = 2

    standingsEU["G2"] = 9
    standingsEU["FNC"] = 8
    standingsEU["OG"] = 8
    standingsEU["MAD"] = 8
    standingsEU["RGE"] = 7
    standingsEU["SK"] = 6
    standingsEU["MSF"] = 5
    standingsEU["VIT"] = 5
    standingsEU["XL"] = 3
    standingsEU["S04"] = 2

    TEAM_STANDINGS.update(standingsEU)
    TEAM_STANDINGS.update(standingsNA)

    TOP = parseRole("top")
    JNG = parseRole("jng")
    MID = parseRole("mid")
    ADC = parseRole("adc")
    SUPP = parseRole("supp")
    TEAMS = parseTeam("teams")
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
                                combos.append([[toplaner[0], jungler[0], midlaner[0], adcarry[0], support[0], squad[0]],
                                               totalPoints])

    bestCombos = sorted(combos, key=lambda x: x[1], reverse=True)
    print(bestCombos[:5])

lookAtPast()
mostLikely()
#mostRobust()











