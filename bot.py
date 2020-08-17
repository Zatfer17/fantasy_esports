import picks

oldLecStandings = "https://web.archive.org/web/20200618203129/https://lol.gamepedia.com/LEC/2020_Season/Summer_Season"
oldLcsStandings = "https://web.archive.org/web/20200619002145/https://lol.gamepedia.com/LCS/2020_Season/Summer_Season"

lecStandings = "https://lol.gamepedia.com/LEC/2020_Season/Summer_Season"
lcsStandings = "https://lol.gamepedia.com/LCS/2020_Season/Summer_Season"

week = "10th"

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
    "teams": 0.7
}

TEAM_STANDINGS = {}

FORBIDDEN = ["Meteos", "Stunt", "Deftly", "Ronaldo", "Wind", "Eika", "Froggen", "Potluck", "Soaz", "P1noy", "Deus", "Jiizuke", "Destiny", "Kumo", "Biofrost", "Mash", "Lourlo", "Nji", "Akaadian"]

WANTED = ['Santorin', 'PowerOfEvil', 'WildTurtle']

picks.mostImportantFirst2(lecStandings, lcsStandings, TEAM_STANDINGS, TEAM_NAMES, week, ROLE_MODIFIERS, DATA, FORBIDDEN, WANTED)
