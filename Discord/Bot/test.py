import json
import requests
import pandas
from bs4 import BeautifulSoup as bs

url = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=12A1D1DE83F9932934EDD6DF2BA00463&steamid=76561197972966230"


r = requests.get(url)
data = r.json()

print(len(data))
results = json.dumps(data, indent=2)
total_kills = data["playerstats"]["stats"][0]["value"]
total_death = data["playerstats"]["stats"][1]["value"]
kd = float(total_kills / total_death)

print(total_kills, total_death, kd)


# url = "https://csgostats.gg/player/76561197972966230"
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# r = requests.get(url, headers=headers)

# soup = bs(r.content)

# print(soup.prettify())
