import pandas as pd
import csv, json, requests

# Data for the 2022-2023 season can be pulled from the following GHub Repo https://github.com/vaastav/Fantasy-Premier-League/tree/master/data/2022-23
# Season parameter should be inputted as "20XX-20XX" dependent on the users preference
def clean_team_data(season):

    # Using pandas read the saved dataframe data from the .csv file. The inputted season in the function will dictate which seasons data is cleaned
    team_df = pd.read_csv("data/"+ season + "/team_data.csv")

    # Filter and pull out the relavent strength stats from the team_df into a new DataFrame
    team_strength_stat = team_df[["short_name", "strength_overall_home", "strength_attack_home", "strength_attack_away", "strength_defence_home", "strength_defence_away"]]
    
    # Save the team strength database into a new .csv file
    team_strength_stat.to_csv("data/"+ season + "/teams_strength_stat.csv")


"""
Similar to the clean_team_data(season) above this new function cleans the player stats database either stored in .csv file or is used in 
conjunction with web_scrape.py which scrapes the data from the FPL website using its API

Function variables: 
- df_column -> a dictionary which contains the:
    1) names of the columns to move
    2) the new name of the column to be displayed in the new DataFrame
    3) the position of the column in the new dataframe

e.g.: 
df_column = {
    "current_name" : ["web_name", "id", "element_type"]
    "new_name" : ["name", "id", "position"]
    "pos" : [0, 1, 2]
}
"""
def clean_player_data(df_column, player_df):
    def test_function(current_column_name, new_column_name, column_position):
        reorder_col = player_df.pop(current_column_name)
        player_df.insert(int(column_position), new_column_name, reorder_col)
    
    for i in range(len(df_columns["pos"])):
        test_function(
            df_columns["current_name"][i],
            df_columns["new_name"][i],
            df_columns["pos"][i]
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




