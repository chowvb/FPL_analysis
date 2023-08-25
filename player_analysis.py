import requests
import pandas as pd
from pprint import pprint
from clean_data import get_gw_data
"""
The following functions are to be used to analyse a players performance using data analytics and basic statistics. 
"""

# Define economy function to calculate point per £1m
def economy(player_id):
    """
    Args:
    Returns:
    Example:
    """
    # Load player database
    players_raw_csv = pd.read_csv("data/2023-2024/players_raw.csv")

    # Filter DataFrame to only show the requested player_id and dataframe index
    player_df = players_raw_csv[players_raw_csv["id"] == int(player_id)].reset_index()

    # Store the total points from player_df 
    total_points = float(player_df.at[0, "total_points"])

    # Store the player value (divide by 10 to make it consistent with the web version of fpl)
    player_value = (player_df.at[0, "now_cost"]/ 10)

    # Calculate the players economy (Number of points scored per £million) and round this ratio to 2dp
    player_economy = round(total_points / player_value, 2)

    # Return the player_economy variable to the user 
    return player_economy

def percentage_matches_started(player_id):
    """
    Prerequisits:
    Args:
    Return:
    Example:
    """
    # Call the get_gw_data()
    player_df = get_gw_data(player_id)

    # Add up the number of starts.
    starts = sum(player_df["starts"])

    # Number of game weeks is the length of the dataframe, get_gw_data() only returns the games that have already been played 
    gw = len(player_df["round"])

    # Calculate the % start rate
    pms = (starts/gw) * 100

    # Return the percentage matches started
    return pms

def player_efficiency(player_id):
    """
    Args:
    Returns:
    Examples:
    """
    # Load player database
    players_raw_csv = pd.read_csv("data/2023-2024/players_raw.csv")

    # Filter the database to the requested player_id passed through the function.
    player_df = players_raw_csv[players_raw_csv["id"] == int(player_id)].reset_index()

    # Retrieve the players total xg over the course of the season so far
    xg = player_df.at[0, "expected_goals"]

    # Retrieve the number of goals the player has scored over the course of the season 
    goals = player_df.at[0, "goals_scored"]

    # Do the same for assists and expected assists 
    xa = player_df.at[0, "expected_assists"]
    assists = player_df.at[0, "assists"]

    
    try: # Use try for the following calculations as some players will return a math error due to the stats they have 
        goals_efficiency = round((goals / xg), 2)
    except:
        goals_efficiency = 0
    
    try:
        assists_efficiency = round((assists / xa), 2)
    except:
        assists_efficiency = 0
        
    # Return the two efficiency variables 
    return goals_efficiency, assists_efficiency

def player_contribution(player_id):
    """
    Args:
    Returns:
    Example:
    """
    # Call copy_premier_league_table from team_analysis.py
    from team_analysis import copy_premier_league_table

    # Create a dictionary which will be converted to a dataframe of the clubs and their corresponding team_ID
    team_replace_dict = {"team_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                         "Team": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford",
                                "Brighton", "Burnley", "Chelsea", "Crystal Palace", 
                                "Everton", "Fulham", "Liverpool", "Luton", "Man City",
                                "Man Utd", "Newcastle", "Nott'm Forrest", "Sheffield Utd",
                                "Spurs", "West Ham","Wolves"]
    }
    team_dict_df = pd.DataFrame(team_replace_dict)

    # Read the players_raw.csv 
    primary_df = pd.read_csv("data/2023-2024/players_raw.csv")

    # Filter to the requested player_id
    primary_df = primary_df[primary_df["id"] == player_id].reset_index(drop = True)

    # Store the number of goal involvements the requested player has (goals + assists)
    goal_involvement = primary_df.at[0, "goals_scored"] + primary_df.at[0, "assists"]
    
    # Request a copy of the premerleague table.
    table_df = copy_premier_league_table()

    # Add the team_dict_df to the premierleague table using "Team" as the common column
    table_df = pd.merge(table_df, team_dict_df, on = "Team")

    # Filter the table to only show the row with the corrosponding team that the player plays for.
    table_df = table_df[table_df["team_id"] == primary_df.at[0, "team"]].reset_index(drop = True)
    
    # Store goals for "F" as team goals 
    team_goals = table_df.at[0, "F"]
    
    # Use Try as wheh writing this code Everton have not scored a goal yet and returns a 0 when using this function
    try :
        percent_goal_involvement = (int(goal_involvement) / int(team_goals)) * 100
    except:
        percent_goal_involvement = 0 

    # Retutn the % goal involvement to the user.
    return percent_goal_involvement