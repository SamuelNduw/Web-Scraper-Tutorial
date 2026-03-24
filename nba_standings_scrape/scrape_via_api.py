import requests
import pandas as pd

url = "https://stats.nba.com/stats/leaguestandingsv3"

params = {
    "GroupBy": "conf",
    "LeagueID": "00",
    "Season": "2025-26",
    "SeasonType": "Regular Season",
    "Section": "overall"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Accept": "application/json"
}

print("Sending request to NBA API...")

response = requests.get(url, headers=headers, params=params, timeout=10)

print("Status code:", response.status_code)

data = response.json()

result = data["resultSets"][0]

columns = result["headers"]
rows = result["rowSet"]

df = pd.DataFrame(rows, columns=columns)

df = df[[
    "Conference",
    "PlayoffRank",
    "TeamCity",
    "TeamName",
    "WINS",
    "LOSSES",
    "WinPCT",
    "HOME",
    "ROAD",
    "L10",
    "CurrentStreak"
]]

df["Team"] = df["TeamCity"] + " " + df["TeamName"]

df = df[[
    "Conference",
    "PlayoffRank",
    "Team",
    "WINS",
    "LOSSES",
    "WinPCT",
    "HOME",
    "ROAD",
    "L10",
    "CurrentStreak"
]]

df.to_csv("nba_standings.csv", index=False)

print("\nSaved to nba_standings.csv")
print(df.head())