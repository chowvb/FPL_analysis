import pandas as pd
import numpy as np 
import os, csv, requests
import matplotlib.pyplot as plt


"""
*** Notes ***
Passing: Done
Defence: Done
Attack: 
Goalkeeping:
"""
team_name = "Manchester City"
# Liverpool defence_index = 50.2
# Arsenal defence_index = 135
# Manchester City defence_index = 117.5
# Burnley = 49.42
def get_passing_stats():
    csv_df = pd.read_csv("fbref_data/team_data/passing.csv", header = [0, 1],index_col= 0)

    squads = csv_df.droplevel(0, axis= 1)
    squads = squads["Squad"]

    total = csv_df["Total"]
    total = total[["Cmp", "Att", "Cmp%"]]
    total = pd.concat([squads, total], axis =1)


    short = csv_df["Short"]
    short = pd.concat([squads, short], axis= 1)

    medium = csv_df["Medium"]
    medium = pd.concat([squads, medium],axis = 1)

    long = csv_df["Long"]
    long = pd.concat([squads, long], axis = 1)

    team_total = total[total["Squad"] == team_name]
    team_short = short[short["Squad"] == team_name]
    team_medium = medium[medium["Squad"] == team_name]
    team_long = long[long["Squad"] == team_name]

    passing_df = pd.concat([team_total, team_short, team_medium, team_long], axis= 0)
    passing_df["Pass_type"] = ["Total", "Short", "Medium", "Long"]
    
    return passing_df

def get_defence_stats(team):
    team_name = team
    csv_df = pd.read_csv("fbref_data/team_data/defence.csv", header = [0, 1], index_col= 0)
    tackles = csv_df["Tackles"]
    challenges = csv_df["Challenges"]
    blocks = csv_df["Blocks"]
    other_columns = csv_df.drop(["Tackles","Challenges","Blocks"], axis = 1).droplevel(0, axis = 1)

    defence_df = pd.concat([other_columns, tackles["Tkl"], blocks["Blocks"], challenges["Tkl%"]], axis = 1)
    defence_df = defence_df[["Squad", "Tkl", "Int", "Blocks", "Clr", "Err", "Tkl%"]]

    team_defence = defence_df[defence_df["Squad"] == team_name]

    pl_table = pd.read_csv("fbref_data/team_data/pl_table.csv")
    team_ga = pl_table[["Squad", "GA"]]
    team_ga = team_ga[team_ga["Squad"] == team_name]

    team_defence = pd.merge(team_defence, team_ga, on = "Squad")

    defence_index = team_defence["Tkl"] + team_defence["Int"] + team_defence["Blocks"] + team_defence["Clr"] - (team_defence["Err"] - (1 / team_defence["Err"]))
    goals_conceded_multiplier = (team_defence["GA"] /2 )

    defence_index =  defence_index / goals_conceded_multiplier
    
    print(defence_index)

