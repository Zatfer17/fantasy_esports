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

        ownRank = TEAM_STANDINGS.get(team)
        rankDiff1 = ownRank - TEAM_STANDINGS.get(enemy1)
        rankDiff2 = ownRank - TEAM_STANDINGS.get(enemy2)

        pts1 = points * (1+(rankDiff1)/10) * ROLE_MODIFIERS.get(role.lower())
        pts2 = points * (1+(rankDiff2)/10) * ROLE_MODIFIERS.get(role.lower())

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

        ownRank = TEAM_STANDINGS.get(name)
        rankDiff1 = ownRank - TEAM_STANDINGS.get(enemy1)
        rankDiff2 = ownRank - TEAM_STANDINGS.get(enemy2)

        pts1 = points * (1 + (rankDiff1) / 10) * ROLE_MODIFIERS.get(role.lower())
        pts2 = points * (1 + (rankDiff2) / 10) * ROLE_MODIFIERS.get(role.lower())

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













