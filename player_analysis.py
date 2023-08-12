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
    players_df.to_csv("data/2023-2024/player_database")
    return players_df

def clean_player_data(df_column, player_df):
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
        "current_name": ["web_name", "id", "element_type"],
        "new_name": ["name", "id", "position"]
    }
    
    # Define a function that rearranges the columns within the player_df DataFrame
    def test_function(current_column_name, new_column_name, column_position):
        reorder_col = player_df.pop(current_column_name)
        player_df.insert(int(column_position), new_column_name, reorder_col)
    
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
    player_df["Position"].replace(position_replace_dict, inplace=True)
    
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


def get_basic_stats_GLK():

    # Filter the players DataFrame by position only showing the players with the GLK label. 
    # The DataFrame does require the user to have previously cleaned the data (Converted the player_element to position and from numbers to poition)
    GLK_df = players_df[players_df["Position"] == "GLK"]

    # Create a list with the relavent stats for the goalkeeper position. Futher stats columns can be included by appending the list below
    GLK_stats = ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists", "clean_sheets", "goals_conceded", "saves"]
    
    # Using the GLK_stats list futher filter the GLK_df down so that it only shows the relavent stats columns.
    GLK_df = GLK_df[GLK_stats]
    return GLK_df


def get_basic_stats_DEF():

    # Filter 
    DEF_df = players_df[players_df["Position"] == "DEF"] 
    DEF_stats = ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists", "clean_sheets", "goals_conceded"]
    return DEF_df


def get_basic_stats_MID():
    MID_df = players_df[players_df["Position"] == "MID"] 
    MID_stats = ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists"]
    return MID_df


def get_basic_stats_FWD():
    FWD_df = players_df[players_df["Position"] == "FWD"] 
    FWD_stats ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists"]
    return FWD_df

"""
player economy function contains a series of simple equations that calculates the effectiveness of players based on the number of points 
that they score compared to other parameters.

Function input variables:
    1) total_points -> total number of points that a player has collated, input should be taken from the player_stats DataFrame or the .csv file for offline analysis.
    2) minutes_played -> total minutes played for the player selected, (personally a better representation of how well players perform as some players will play lots of matches in a season as last minute substitutions)
    3) now_cost -> how much the player currently costs as this can fluctuate during the season due to performance, this variable shouble be taken from the most recent version of the DataFrame.

Notes:  
"""
def player_economy(total_points, minutes_played, now_cost, goals_scored, assists):
    
    # ppm_economy (points per minute) calculates the average number of points that a player will score per the amount of time they play
    ppm_economy = int(total_points)/int(minutes_played)

    # ppc_economy (point per cost) divide minutes played by 10 to create the same format as FPL website. 
    ppc_economy = total_points/(now_cost/10)

    # mpg_economy (minutes per goal) 
    mpg_economy = goals_scored/minutes_played
    
    # mpa_economy (minutes per assist)
    mpa_economy = assists/minutes_played
