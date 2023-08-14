import pandas as pd 
import requests, csv, json


def update_player_data():
    """
Requests current seasons stats from FPL api. It filters the scraped results to only player "elements"
stats that correspond to players only rather than teams.
Saves the database into a .csv file for locally stored data for offline analysis. 
"""
    # Set the base URL for the fantasy football api
    base_link = "https://fantasy.premierleague.com/api/"

    # Add the the same extension "bootstrap-static to collate the FPL data
    response = requests.get(base_link + "bootstrap-static/")

    # store the websraped data as a .json format 
    response = json.loads(response.content)

    # filter the json results to "element" this represents the data linked to players. 
    players = response["elements"]

    # Convert the .json results into a pandas DataFrame for easier data analysis formatting. 
    players_df = pd.DataFrame(players)

    # Save the DataFrame into a .csv file to sotere the data for offline analysis. 
    players_df.to_csv("data/2023-2024/player_database.csv")
    return players_df

def clean_player_data(player_df):
    """
Similar to the clean_team_data(season) above this new function cleans the player stats database either stored in .csv file or is used in 
conjunction with web_scrape.py which scrapes the data from the FPL website using its API

Function variables: 
- df_column -> a dictionary which contains the:
    1) names of the columns to move
    2) the new name of the column to be displayed in the new DataFrame
"""
    # Define the columns to be rearranged 
    df_columns = {
        "current_name": ["web_name" , "team", "id", "element_type", "now_cost"],
        "new_name": ["name", "team" , "id", "position", "price"]
    }
    
    # Define a function that rearranges the columns within the player_df DataFrame
    def test_function(current_column_name, new_column_name, column_position):
        reorder_col = player_df.pop(current_column_name)
        player_df.insert(column_position, new_column_name, reorder_col)
    
    # Iterate over the length of column_df and call test_function() for each iteration.
    for i in range(len(df_columns["new_name"])):
        test_function(
            df_columns["current_name"][i],
            df_columns["new_name"][i],
            i
            )
        
    # Create a dictionary of the position of the players in the raw format and the corrosponding position that that the players play in. 
    position_replace_dict = { 1: "GLK", 2: "DEF", 3 : "MID", 4: "FWD"}

    # Replace the numbers within the "Position" column with the corrosponding positions that the players are positioned. 
    player_df["position"].replace(position_replace_dict, inplace=True)
    
    # Create a dictionary of the teams and the correspoinding team codes for each of the players 
    team_replace_dict = { 
        1 : "Arsenal",
        2 : "Aston Villa",
        3 : "Bournemouth",
        4 : "Brentford",
        5 : "Bighton",
        6 : "Burnley",
        7 : "Chelsea",
        8 : "Crystal Palace", 
        9 : "Everton",
        10 : "Fulham",
        11 : "Liverpool",
        12 : "Luton",
        13 : "Man City",
        14 : "Man Utd",
        15 : "Newcastle",
        16 : "Nott'm Forrest",
        17 : "Sheffield Utd",
        18 : "Spurs",
        19 : "West Ham",
        20 : "Wolves"
    }

    # Replace the numbers in the team column with the name of the clubs that the players play for.
    player_df["team"].replace(team_replace_dict, inplace = True)
    return player_df


def get_basic_stats_GLK(players_df):

    # Filter the players DataFrame by position only showing the players with the GLK label. 
    # The DataFrame does require the user to have previously cleaned the data (Converted the player_element to position and from numbers to poition)
    GLK_df = players_df[players_df["position"] == "GLK"]

    # Create a list with the relavent stats for the goalkeeper position. Futher stats columns can be included by appending the list below
    GLK_stats = ["name", "team", "id", "position", "price", "total_points", "bonus", "goals_scored", "assists", "clean_sheets", "goals_conceded", "saves"]
    
    # Using the GLK_stats list futher filter the GLK_df down so that it only shows the relavent stats columns.
    GLK_stats_df = GLK_df[GLK_stats]

    return GLK_stats_df


def get_basic_stats_DEF(players_df):

    # Filter 
    DEF_df = players_df[players_df["position"] == "DEF"] 
    DEF_stats = ["name", "team", "id", "position", "price" ,  "total_points", "bonus", "goals_scored", "assists", "clean_sheets", "goals_conceded"]
    DEF_stats_df = DEF_df[DEF_stats]
    
    return DEF_stats_df


def get_basic_stats_MID(players_df):
    MID_df = players_df[players_df["position"] == "MID"] 
    MID_stats = ["name", "team", "id", "position", "price" ,"total_points", "bonus", "goals_scored", "assists"]
    MID_stats_df = MID_df[MID_stats]
    return MID_stats_df


def get_basic_stats_FWD(players_df):
    FWD_df = players_df[players_df["position"] == "FWD"] 
    FWD_stats = ["name", "team" , "id", "position","price", "total_points", "bonus", "goals_scored", "assists"]
    FWD_stats_df = FWD_df[FWD_stats]
    return FWD_stats_df


def get_basic_stats_glob(position, players_df):

    df = players_df[players_df["position"] == position]
    
    # Each positions stats to pull in a list
    base_stats = ["name", "team", "id", "position", "price", "total_points", "bonus"]
    GLK_stats = ["goals_scored", "assists", "clean_sheets", "goals_conceded", "saves"]
    DEF_stats = ["goals_scored", "assists", "clean_sheets", "goals_conceded"]
    MID_stats = ["goals_scored", "assists", "clean_sheets"]
    FWD_stats = ["goals_scored", "assists"]

    if position == "GLK":
        df_stats = df[GLK_stats]
    elif position == "DEF":
        df_stats = df[DEF_stats]
    elif position == "MID":
        df_stats = df[MID_stats]
    else:
        df_stats = df[FWD_stats]
    
    
    return df_stats