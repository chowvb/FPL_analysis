import requests
import pandas as pd
from pprint import pprint

"""
The following functions are to be utilised with main_function to retrieve statistics for a desired player based off their player id
"""
url = "https://fantasy.premierleague.com/api/"

def gw_stats(player_id):
    # Obtain the web_name of a player by inputting their player_id
    def get_name(player_id):
        # Open the raw player database csv file.
        player_id_csv = pd.read_csv("data/2023-2024/players_raw.csv")

        # Filter the database to players that match the player_id
        player_name = player_id_csv[player_id_csv["id"] == int(player_id)].reset_index()

        # Obtain the web_name for the player (Note: first and second names shouldn't be used as many players (Brazilians) don't always go by their given names)
        player_name = player_name.at[0,"web_name"]

        # Return the player name
        return player_name

    # Obtain player performance statistics from the element_summary endpoint based of a player_id number
    def get_player_performance(player_id):
        # Add the endpoint name
        endpoint = "element-summary/"

        # Scrape the data off fpl API combining the url + endpoint + player_id
        response = requests.get(url + endpoint + str(player_id) + "/").json()

        # Convert the json format to a DataFrame, filtering through "history"
        df = pd.DataFrame(response["history"])

        # Call the get_name() function defined above to get the player name corresponding to the player_id
        player_name = get_name(player_id)

        # Create a dictionary to replace the id number with the player name
        full_name = {player_id: player_name}

        # Replace the player number with the player name
        df["element"].replace(full_name, inplace= True)

        # Return the formatted dataframe
        return df

    # Collect individual performance based off the game week and player_id 
    def get_weekly_performance(player_id, GW_number):
        # Define the endpoint to be used
        endpoint = "event/"+ str(GW_number) + "/live/"

        # Request data from fpl apy
        response = requests.get(url + endpoint).json()

        # Convert json to dataframe filtering through "elements" (players)
        player_df = pd.DataFrame(response["elements"])
        
        # Filter and locate the desired player by using the player_id passed through the function
        player_df = player_df[player_df["id"] == player_id].reset_index()

        # Extract the data from the "stats" column
        player_df = player_df.at[0, "stats"]
        player_df = pd.DataFrame(player_df, index =[0])
        # Add a column called round with the value of the game week. This will be needed to merge the dataframe to the player_performance dataframe above
        player_df["round"] = GW_number

        # Return the player dataframe
        return player_df
    
    # call get_player_performance to retrieve recent performance
    df = get_player_performance(player_id)

    # Create an empty DataFrame
    player_df = pd.DataFrame()

    # Loop through the number of games played 
    for gw in df["round"]:
        # Call the get_weekly_performance and store the results into a DataFrame
        performance_df = get_weekly_performance(player_id, gw)

        # Concat to the empty DataFrame
        player_df = pd.concat([player_df,performance_df], ignore_index= True)

    # Merge the two dataframes with "round" as the common columns
    merged_df = pd.merge(df,player_df, on = ["round","assists","bonus", "bps","clean_sheets", "creativity",
                                             "expected_assists", "expected_goal_involvements", "expected_goals",
                                             "expected_goals_conceded", "goals_conceded", "goals_scored", "ict_index",
                                             "influence", "minutes", "own_goals", "penalties_missed","penalties_saved",
                                             "red_cards","saves","starts","threat", "total_points", "yellow_cards"])

    return merged_df

# Call the main function with desired player_id (308 = Mo Salah)
#df = gw_stats(308)

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
    player_df = gw_stats(player_id)
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