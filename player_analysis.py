import requests
import pandas as pd
from pprint import pprint

"""
The following functions are to be utilised with main_function to retrieve statistics for a desired player based off their player id
"""
url = "https://fantasy.premierleague.com/api/"

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


def main_function(player_id):
    # Get John McGinn's recent performance
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
df = main_function(308)

"""
The following functions are to be used to analyse a players performance using data analytics and basic statistics. 
"""

# Define economy function to calculate point per £1m
def economy(player_id):
    # Load player database
    players_raw_csv = pd.read_csv("data/2023-2024/players_raw.csv")
    player_df = players_raw_csv[players_raw_csv["id"] == int(player_id)].reset_index()
    total_points = float(player_df.at[0, "total_points"])
    player_value = (player_df.at[0, "value"]/ 10)
    player_economy = total_points / player_value
    return player_economy

def percentage_matches_started(player_id):
    player_df = main_function(player_id)
    starts = sum(player_df["starts"])
    gw = len(player_df["round"])
    pms = (starts/gw) * 100
    return pms
