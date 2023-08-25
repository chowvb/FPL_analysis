import requests
import pandas as pd
from pprint import pprint
from clean_data import get_gw_data
"""
The following functions are to be used to analyse a players performance using data analytics and basic statistics. 
"""

# Define economy function to calculate point per £1m
def economy(player_id):
    # Load player database
    players_raw_csv = pd.read_csv("data/2023-2024/players_raw.csv")
    player_df = players_raw_csv[players_raw_csv["id"] == int(player_id)].reset_index()
    total_points = float(player_df.at[0, "total_points"])
    player_value = (player_df.at[0, "now_cost"]/ 10)
    player_economy = round(total_points / player_value, 2)
    return player_economy

def percentage_matches_started(player_id):
    player_df = get_gw_data(player_id)
    starts = sum(player_df["starts"])
    gw = len(player_df["round"])
    pms = (starts/gw) * 100
    return pms

def player_efficiency(player_id):
    # Load player database
    players_raw_csv = pd.read_csv("data/2023-2024/players_raw.csv")
    player_df = players_raw_csv[players_raw_csv["id"] == int(player_id)].reset_index()

    xg = player_df.at[0, "expected_goals"]
    goals = player_df.at[0, "goals_scored"]
    xa = player_df.at[0, "expected_assists"]
    assists = player_df.at[0, "assists"]

    try:
        goals_efficiency = round((goals / xg), 2)
    except:
        goals_efficiency = 0
    
    try:
        assists_efficiency = round((assists / xa), 2)
    except:
        assists_efficiency = 0
        
    return goals_efficiency, assists_efficiency

def player_contribution(player_id):
    from team_analysis import copy_premier_league_table

    team_replace_dict = {"team_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                         "Team": 
                         ["Arsenal",
                            "Aston Villa",
                            "Bournemouth",
                            "Brentford",
                            "Brighton",
                            "Burnley",
                            "Chelsea",
                            "Crystal Palace", 
                            "Everton",
                            "Fulham",
                            "Liverpool",
                            "Luton",
                            "Man City",
                            "Man Utd",
                            "Newcastle",
                            "Nott'm Forrest",
                            "Sheffield Utd",
                            "Spurs",
                            "West Ham",
                            "Wolves"]
    }
    team_dict_df = pd.DataFrame(team_replace_dict)

    primary_df = pd.read_csv("data/2023-2024/players_raw.csv")
    primary_df = primary_df[primary_df["id"] == player_id].reset_index(drop = True)
    goal_involvement = primary_df.at[0, "goals_scored"] + primary_df.at[0, "assists"]
    
    table_df = copy_premier_league_table()
    table_df = pd.merge(table_df, team_dict_df, on = "Team")
    table_df = table_df[table_df["team_id"] == primary_df.at[0, "team"]].reset_index(drop = True)
    team_goals = table_df.at[0, "F"]
    
    try :
        percent_goal_involvement = (int(goal_involvement) / int(team_goals)) * 100
    except:
        percent_goal_involvement = 0 

    return percent_goal_involvement