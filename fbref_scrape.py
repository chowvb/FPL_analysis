import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utility import team_replace_dict_fbref, team_replace_dict2

r = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats/")
soup = BeautifulSoup(r.text)
standings_table = soup.select("table.stats_table")[0]
teams = standings_table.find_all("a")
links = [l.get("href") for l in teams]
team_urls = [f"https://fbref.com{l}" for l in links]
teams_list = []
for i, team in enumerate(teams):
    teams_list.append(teams[i].text)
team_df = pd.DataFrame({
    "Team": teams_list,
    "Link": team_urls
    })
team_df = team_df[team_df["Link"].str.contains("/squads/")]
team_df["Path"] = [urlparse(url).path for url in team_df["Link"]]
team_df = team_df.join(team_df["Path"].str.split("/", expand = True).add_prefix("Path_"))
team_df = team_df.rename(columns={"Path_3": "unique_team_id", "Path_4": "extension"})
team_df = team_df[["Team", "unique_team_id", "extension", "Link"]]


r = requests.get("https://fbref.com/en/comps/9//wages/Premier-League-Wages/")
soup = BeautifulSoup(r.text)
table = soup.select("table.stats_table")[1]
players = table.find_all("a")
links = [l.get("href") for l in players]
player_urls = [f"https://fbref.com{l}" for l in links]
player_list = []
for i, player in enumerate(players):
    player_list.append(players[i].text)
players_df = pd.DataFrame({
    "Player" : player_list,
    "Link" : player_urls 
    })
players_df = players_df[players_df["Link"].str.contains("/players/")]
players_df["Path"] = [urlparse(url).path for url in players_df["Link"]]
players_df = players_df.join(players_df["Path"].str.split("/", expand=True).add_prefix("Path_"))
players_df = players_df.rename(columns={"Path_3": "unique_player_id", "Path_4": "extension"})
players_df = players_df[["Player", "unique_player_id", "extension", "Link"]]

fpl_team_id = pd.DataFrame(team_replace_dict_fbref)
fpl_team_name = pd.DataFrame(team_replace_dict2)
merged_team_df = team_df.merge(fpl_team_id, on= "Team")
merged_team_df = merged_team_df.merge(fpl_team_name, left_on = "fpl_team_id", right_on= "team_id")
merged_team_df = merged_team_df.drop(columns=["team_id"]).rename(columns={"Team_x" : "Team","Team_y": "fpl_team"})