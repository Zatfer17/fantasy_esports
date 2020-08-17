import pandas as pd
import requests
from bs4 import BeautifulSoup

def parseRole(role, week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA):
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

        ownRank = TEAM_STANDINGS.get(team)[0]

        rankDiff1 = ownRank - TEAM_STANDINGS.get(enemy1)[0]
        rankDiff2 = ownRank - TEAM_STANDINGS.get(enemy2)[0]

        ownForm = TEAM_STANDINGS.get(team)[1]

        pts1 = points * (1+(rankDiff1)/10) * (1+(ownForm)/10) * ROLE_MODIFIERS.get(role.lower())
        pts2 = points * (1+(rankDiff2)/10) * (1+(ownForm)/10) * ROLE_MODIFIERS.get(role.lower())

        totalSafety = rankDiff1 + rankDiff2
        safetyForMoney = totalSafety / salary
        totalPts = pts1 + pts2
        if totalPts != 0:
            valueForMoney = totalPts / salary
        else:
            valueForMoney = 0

        DATA.append(
            [role, name, team, salary, points, enemy1, pts1, enemy2, pts2, totalPts, valueForMoney, totalSafety,
             safetyForMoney])
        table.append([name, salary, totalPts, valueForMoney, totalSafety, safetyForMoney])
    return table

def parseTeam(role, week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA):
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

        ownRank = TEAM_STANDINGS.get(name)[0]
        rankDiff1 = ownRank - TEAM_STANDINGS.get(enemy1)[0]
        rankDiff2 = ownRank - TEAM_STANDINGS.get(enemy2)[0]

        ownForm = TEAM_STANDINGS.get(name)[1]

        pts1 = points * (1 + (rankDiff1) / 10) * (1 + (ownForm) / 10) * ROLE_MODIFIERS.get(role.lower())
        pts2 = points * (1 + (rankDiff2) / 10) * (1 + (ownForm) / 10) * ROLE_MODIFIERS.get(role.lower())

        totalSafety = rankDiff1 + rankDiff2
        safetyForMoney = totalSafety / salary
        totalPts = pts1 + pts2
        if totalPts != 0:
            valueForMoney = totalPts / salary
        else:
            valueForMoney = 0

        DATA.append(
            [role, name, team, salary, points, enemy1, pts1, enemy2, pts2, totalPts, valueForMoney, totalSafety, safetyForMoney])
        table.append([name, salary, totalPts, valueForMoney, totalSafety, safetyForMoney])
    return table


def parseRole2(role, week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA):
    table = []
    numLines = sum(1 for line in open("data/" + week + "_week/" + role + ".txt", "r")) - 1
    file = open("data/" + week + "_week/" + role + ".txt", "r")
    file.seek(1)
    for i in range(0, int(numLines / 8)):
        row = [next(file) for x in range(8)]
        role = role.upper()
        name = row[1].replace("\n", "")
        team = row[3].replace("\n", "")
        salary = float(row[5].replace("\n", "").replace("$", "").replace(".000", ""))
        points = float(row[6].replace("\n", "").replace("-", "0"))

        if "GG" in team:
            enemy = "TSM"
        elif "TSM" in team:
            enemy = "GG"
        elif "EG" in team:
            enemy = "FLY"
        else:
            enemy = "EG"

        ownRank = TEAM_STANDINGS.get(team)[0]
        rankDiff = ownRank - TEAM_STANDINGS.get(enemy)[0]

        pts = points * (1 + (rankDiff) / 10) * ROLE_MODIFIERS.get(role.lower())

        totalSafety = rankDiff
        safetyForMoney = totalSafety / salary
        totalPts = pts
        if totalPts != 0:
            valueForMoney = totalPts / salary
        else:
            valueForMoney = 0

        DATA.append(
            [role, name, team, salary, points, enemy, pts, totalPts, valueForMoney, totalSafety,
             safetyForMoney])
        table.append([name, salary, totalPts, valueForMoney, totalSafety, safetyForMoney])
    return table


def parseTeam2(role, week, TEAM_STANDINGS, ROLE_MODIFIERS, DATA):
    table = []
    numLines = sum(1 for line in open("data/" + week + "_week/" + role + ".txt", "r")) - 1
    file = open("data/" + week + "_week/" + role + ".txt", "r")
    file.seek(1)
    for i in range(0, int(numLines / 12)):
        row = [next(file) for x in range(8)]
        role = role.upper()
        name = row[1].replace("\n", "")
        team = row[3].replace("\n", "")
        salary = float(row[4].replace("\n", "").replace("$", "").replace(".000", ""))
        points = float(row[5].replace("\n", "").replace("-", "0"))

        if "GG" in name:
            enemy = "TSM"
        elif "TSM" in name:
            enemy = "GG"
        elif "EG" in name:
            enemy = "FLY"
        else:
            enemy = "EG"

        ownRank = TEAM_STANDINGS.get(name)[0]
        rankDiff = ownRank - TEAM_STANDINGS.get(enemy)[0]

        pts = points * (1 + (rankDiff) / 10) * ROLE_MODIFIERS.get(role.lower())

        totalSafety = rankDiff
        safetyForMoney = totalSafety / salary
        totalPts = pts
        if totalPts != 0:
            valueForMoney = totalPts / salary
        else:
            valueForMoney = 0

        DATA.append(
            [role, name, team, salary, points, enemy, pts, totalPts, valueForMoney, totalSafety,
             safetyForMoney])
        table.append([name, salary, totalPts, valueForMoney, totalSafety, safetyForMoney])
    return table

def writeData(week, DATA):
    df = pd.DataFrame(DATA)
    df.to_excel(excel_writer="outputs/" + week + "_week.xlsx")

def updateStandings(lecStandings, lcsStandings, TEAM_STANDINGS, TEAM_NAMES):
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
        streak = team.contents[4].text
        if "L" in streak:
            streak = - int(streak.replace("L", ""))
        else:
            streak = int(streak.replace("W", ""))
        TEAM_STANDINGS[TEAM_NAMES.get(name)] = (11 - position), streak

    soup = BeautifulSoup(lcs, "html.parser")
    rows = soup.findAll("div", {"class": "standings-outer-div"})
    teamsContainer = rows.pop()
    teams = teamsContainer.contents[0].contents[0].contents[0]
    for i in range(2, 12):
        team = teams.contents[i]
        name = team.contents[1].contents[0].contents[1].text
        position = int(team.contents[0].text)
        streak = team.contents[4].text
        if "L" in streak:
            streak = - int(streak.replace("L", ""))
        else:
            streak = int(streak.replace("W", ""))
        TEAM_STANDINGS[TEAM_NAMES.get(name)] = (11 - position), streak

    print(TEAM_STANDINGS)












