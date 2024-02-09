import team_analysis as ta
import player_analysis as pa
import pandas as pd
import utility
from IPython.display import display
from data_visualisation_tools import get_team_strength_stats
import numpy as np
import matplotlib.pyplot as plt

"""
***Notes***

Script function -
    - Takes the latest result in the premier league and creates post match analysis. 

Requires internet connection as functions used within this script utilises web scraping to obtain match data from fbref.com and FantasyPremierLeague.com

"""

team_name = "Liverpool" # FPL team name
team_id = 11 # Corresponds to team_id in FPL
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def get_match_report():
    r = requests.get("https://fbref.com/en/squads/822bd0ba/Liverpool-Stats")
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find_all("div", attrs={"data-template":"Partials/Teams/Summary"})
    soup2 = BeautifulSoup(str(table))
    for i in soup2.find_all("a", attrs={"href": re.compile("/en/matches/")}):
        match_link = i.get("href")
        link = f"https://fbref.com{match_link}"
    return link

fixtures = pd.read_csv("data/2023-2024/fixtures.csv", index_col= 0)
team_fixtures_h = fixtures[fixtures["Home"] == team_name]
team_fixtures_a = fixtures[fixtures["Away"] == team_name]
team_fixtures = pd.concat([team_fixtures_h,team_fixtures_a])
team_fixtures = team_fixtures.sort_values(by = "GW", ascending= True)

team_fixtures = team_fixtures.dropna()
latest_match = team_fixtures.tail(1).reset_index()
if latest_match.at[0, "Home"] == team_name:
    opponent_team = latest_match.at[0, "Away"]
else:
    opponent_team = latest_match.at[0, "Home"]

print(opponent_team)

pl_team_id = pd.read_csv("fbref_data/team_data/team_id.csv", index_col= 0)
opponent_team_id = pl_team_id[pl_team_id["fpl_team"] == opponent_team].reset_index()
opponent_team_id = opponent_team_id.at[0, "unique_team_id"]

home_team_id = pl_team_id[pl_team_id["fpl_team"] == team_name].reset_index()
home_team_id = home_team_id.at[0, "unique_team_id"]

match_report_link = get_match_report()
r = requests.get(str(match_report_link))
soup = BeautifulSoup(r.text, "html.parser")
opponent_table = soup.find("table", {"id": f"stats_{opponent_team_id}_summary"})
opponent_stats_df = pd.read_html(str(opponent_table))[0]


team_table = soup.find("table", {"id": f"stats_{home_team_id}_summary"})
team_stats_df = pd.read_html(str(team_table))[0]

# Combine summary stats for both teams
summary_team = team_stats_df.tail(1).reset_index(drop = True)
summary_team.drop(summary_team.iloc[:,0:10], inplace = True, axis = 1)
summary_team = summary_team.droplevel(0, axis = 1)
summary_team.insert(loc = 0,
                    column= "Team",
                    value = team_name)

summary_opponent = opponent_stats_df.tail(1).reset_index(drop= True)
summary_opponent.drop(summary_opponent.iloc[:,0:10], inplace = True, axis = 1)
summary_opponent =summary_opponent.droplevel(0, axis = 1)
summary_opponent.insert(loc = 0, 
                        column= "Team",
                        value= opponent_team)

h2h_summary = pd.concat([summary_team,summary_opponent]).reset_index(drop= True)
h2h_summary = h2h_summary[["Team", "Sh", "SoT", "Tkl", "Int", "Blocks"]]
h2h_summary = h2h_summary.T.rename(columns=h2h_summary["Team"]).tail(-1)

categories = h2h_summary.index.tolist()
liverpool_data = h2h_summary[team_name].values
opponent_data = h2h_summary[opponent_team].values
import plotly.graph_objects as go 

# Define Figure
fig = go.Figure()

# Add the plot for team1
fig.add_trace(go.Scatterpolar(
    r = liverpool_data,
    theta = categories,
    fill = "toself",
    name = team_name
))

# Add the plot for team2
fig.add_trace(go.Scatterpolar(
    r = opponent_data,
    theta = categories,
    fill = "toself",
    name = opponent_team
))
fig.show()

import seaborn as sns
import matplotlib as mpl 
sns.set()

font_color = '#525252'
hfont = {'fontname':'Calibri'}
facecolor = '#eaeaf2'
color_red = '#fd625e'
color_blue = '#01b8aa'
index = h2h_summary.index
column0 = h2h_summary[team_name]
column1 = h2h_summary[opponent_team]
title0 = team_name
title1 = opponent_team

fig, axes = plt.subplots(figsize=(10,5), facecolor=facecolor, ncols=2, sharey=True)
fig.tight_layout()
axes[0].barh(index, column0, align='center', color=color_red, zorder=10)
axes[0].set_title(title0, fontsize=18, pad=15, color=color_red, **hfont)
axes[1].barh(index, column1, align='center', color=color_blue, zorder=10)
axes[1].set_title(title1, fontsize=18, pad=15, color=color_blue, **hfont)
# If you have positive numbers and want to invert the x-axis of the left plot
axes[0].invert_xaxis() 

# To show data from highest to lowest
plt.gca().invert_yaxis()

axes[0].set(yticks=h2h_summary.index, yticklabels=h2h_summary.index)
axes[0].yaxis.tick_left()
axes[0].tick_params(axis='y', colors='Black') # tick color