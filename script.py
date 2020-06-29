from bs4 import BeautifulSoup
import pandas as pd

TEAM_STANDINGS = {
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

def getName(name):
    name = str(name)
    end = len(name) - 6
    return name[24:end]

def getTeam(team):
    team = str(team)
    start = team.find(">")
    toReturn = team[start:start + 4]
    toReturn = toReturn.replace(">", "")
    toReturn = toReturn.replace("<", "")
    return toReturn.replace(">", "")

def getPosition(position):
    position = str(position)
    start = position.find("<title>") + 7
    end = position.find("</title>")
    return position[start:end]

def getSalary(salary):
    salary = str(salary)
    end = len(salary) - 13
    salary = salary[32:end]
    return float(salary.replace("$",""))

def getTeamSalary(salary):
    salary = str(salary)
    end = len(salary) - 14
    salary = salary[34:end]
    return float(salary.replace("$",""))

def getPts(pts):
    pts = str(pts)
    end = len(pts) - 6
    toReturn = pts[5:end]
    if "-" in toReturn:
        return 0.0
    else:
        return float(toReturn)

def getKda(kda):
    kda = str(kda)
    end = len(kda) - 6
    toReturn = kda[5:end]
    if "-" in toReturn:
        return 0.0
    else:
        return float(toReturn)

def getWin(agd):
    agd = str(agd)
    end = len(agd) - 7
    return agd[5:end]

def getAgd(agd):
    agd = str(agd)
    end = len(agd) - 6
    return float(agd[5:end].replace(":", "."))

def getGame(game):
    game = str(game)
    end1 = game.find(">")-1
    matchup = game[12:end1]
    start2 = game.find("title=")+10
    opponent = game[start2:start2+3]
    opponent = opponent.replace("<", "")
    return matchup, opponent

def getTeamGame(game):
    game = str(game)
    end1 = game.find("</div>")
    opponent = game[36:end1]
    start2 = end1 + 37
    matchup = game[start2:start2 + 4]
    matchup = matchup.replace("<", "")
    return matchup, opponent

def exportPlayers():
    soup = BeautifulSoup(open("players.html"), "html.parser")
    rows = soup.findAll("div", {"class": "playerDataRow"})
    players = []
    for row in rows:
        name = getName(row.contents[5])
        team = getTeam(row.contents[11])
        position = getPosition(row.contents[13])
        salary = getSalary(row.contents[17])
        pts = getPts(row.contents[19])
        kda = getKda(row.contents[21])
        game1 = getGame(row.contents[23])
        game2 = getGame(row.contents[25])
        rank = float(TEAM_STANDINGS.get(team))
        players.append([name, team, position, salary, pts, rank])
    df = pd.DataFrame(players)
    df.to_excel(excel_writer = "players.xlsx")

def exportTeams():
    soup = BeautifulSoup(open("teams.html"), "html.parser")
    rows = soup.findAll("div", {"class": "playerDataRow"})
    teams = []
    for row in rows:
        name = getTeam(row.contents[5])
        salary = getTeamSalary(row.contents[13])
        pts = getPts(row.contents[15])
        win = getWin(row.contents[17])
        agd = getAgd(row.contents[19])
        rank = float(TEAM_STANDINGS.get(name))
        teams.append([name, salary, pts, rank])
    df = pd.DataFrame(teams)
    df.to_excel(excel_writer = "teams.xlsx")

exportTeams()
exportPlayers()

