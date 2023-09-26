"""
This whole script is to be run to update all of the player databases that are stored onto the local disk.

This script does not require any arguments and will self direct to the corresponding endpoints to request FPL data.
"""

import requests
import pandas as pd 
import utility 


"""
scrape_data() - collects player data from FPL bootstrap and saves three seperate .csv files 
    - players_raw.csv
        all current data of fpl players upto the most recent game weeks. Raw data with no data cleaning.
    
    - player_idlist.csv
        contains all the players in the fpl database with their:
            - first name
            - second name
            - web name -> how they are commonly refered as (Brazilian players generally have different web names to first and last names)
            - id -> the player ID number corresponding to a specific player during the FPL season 
            - team -> The team that the player currently plays for. 
        This database will contain players that have already moved away from the football clubs during the season 
    
    - cleaned_players.csv
        This file contains the key stats that will be used for data analysis. The data is in a similar format to the previous seasons cleaned_players.csv file
"""
def scrape_data():
    # Create a dictionary of the position of the players in the raw format and the corrosponding position that that the players play in. 
    position_replace_dict = { 1: "GLK", 2: "DEF", 3 : "MID", 4: "FWD"}   
    team_replace_dict = utility.team_replace_dict
    # Define API endpoint
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"

    # Connect with the API and save the data as a .json()
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Filter through the .json() for "elements" == "players"
    players = data["elements"]

    # Convert the .json() into a pandas DataFrame for easier analysis. 
    players_df = pd.DataFrame(players)

    # Save the DataFrame to .csv file for offline analysis 
    players_df.to_csv("data/2023-2024/players_raw.csv", index = False)

    # Create a DataFrame with only the id, Name, team and position and save to a .csv file for offline analysis
    player_id_df = players_df[["first_name", "second_name", "id", "team"]]
    player_id_df["team"].replace(utility.team_replace_dict, inplace = True)
    player_id_df.to_csv("data/2023-2024/player_idlist.csv", index=False)

    # Create a DataFrame to the same format as 2022-2023/cleaned_players.csv format for easy analysis and comparison to previous season.
    cleaned_players_df = players_df[["first_name", "second_name", "team", "goals_scored", "assists", "total_points",
                                "minutes", "goals_conceded", "creativity", "influence", "threat", "bonus",
                                "bps", "ict_index", "clean_sheets", "red_cards", "yellow_cards", "selected_by_percent",
                                "now_cost", "element_type"]]

    # Replace element_type numbers with corresponding positions
    cleaned_players_df["element_type"].replace(position_replace_dict, inplace = True)
    cleaned_players_df["team"].replace(team_replace_dict, inplace = True)

    # Save the cleaned_players_df to a .csv file for offline analysis
    cleaned_players_df.to_csv("data/2023-2024/cleaned_players.csv", index = False)

"""
get_gw_data(player_id) - takes a players ID number as the argument and requests all the gameweek data for the inputted player ID
    - This function is a prerequisite for get_all_gw_data() later in this python script. 
"""
def get_gw_data(player_id):
    # Read the player_id_list to obtain player names and clubs for the corrosponding player_id number
    player_id_list = pd.read_csv("data/2023-2024/player_idlist.csv")

    # Set the API url
    url = "https://fantasy.premierleague.com/api/"

    # Set the endpoint that retrieves game week data for individual players 
    endpoint = "element-summary/"

    # Send a GET requst to the API url with the player ID inputted into the address
    response = requests.get(url + endpoint+ str(player_id)+ "/").json()

    # Convert the response from a json to a pandas dataframe whilst filtering to history (returns games that have already been played)
    df = pd.DataFrame(response["history"])

    # Filter the player_id_list dataframe defined at the start to only show the requested player (player_id) and reset the index of the new dataframe
    player_id = player_id_list[player_id_list["id"] == int(player_id)].reset_index()

    # Obtain the player name
    player_first_name = player_id.at[0,"first_name"]
    player_second_name = player_id.at[0,"second_name"]

    # Join the first name and second name (we do this because all the previous merged_gw.csv files have the player name in this format)
    player_name = player_first_name + " " + player_second_name

    # Retrieve the team that the requested player plays for 
    team_name = player_id.at[0,"team"]

    # Change all the names in the column "element" to the requested players first and second name combined 
    df["element"] = player_name

    # Change the elements columns name to "name" so it is consisten to the other merged_gw files.
    df.rename(columns={"element":"name"}, inplace=True)

    # Add the team that the player play for into the dataframe, some historical data doesn't have this but the most recent seasons do. 
    df["team"] = team_name

    # Replace Opponent team from id number to name
    team_id = pd.DataFrame(utility.team_replace_dict2)
    team_id = team_id.rename(columns={"team_id": "opponent_team", "Team": "opponent"})

    result_df = pd.merge(df, team_id, on = "opponent_team")
    result_df.drop("opponent_team", axis = 1, inplace = True)
    result_df = result_df.rename(columns={"opponent": "opponent_team"})

    # Return the DataFrame back to the user.
    return result_df
"""
get_all_gw_data() - takes the prerequisite function (get_gw_data()) and loops through all of the players in the player_idlist.csv file.
    - The function returns every game week data for each player.
    - Saves the collated data into a csv file (merged_gw.csv)

*** Note ***
This function can take a long time to run, especially as the season progresses and more fixtures are played.
"""
def get_all_gw_data():
    # Load player_idlist.csv
    player_id_list = pd.read_csv("data/2023-2024/player_idlist.csv")
    
    # Create an empty dataframe which will be used to contain all available players in FPL and their weekly performance 
    merged_gw = pd.DataFrame()

    # iterate through the players_idlist.csv file.
    for i, id in enumerate(player_id_list["id"]):
        # This print statement is present to show progress as this function takes a long time to iterate through especially as the season progresses and more games are played 
        print("Loading Player: "+ str(i) + "/" + str(len(player_id_list)-1))

        # Call the get_gw_data() function that is defined above to get each players game week performance 
        df = get_gw_data(id)

        # Concatinate the dataframe with the empty merged_gw dataframe to continually add data do the dataframe for each of the itterations. 
        merged_gw = pd.concat([merged_gw, df])
    
    # Save the dataframe as a csv file on the local machine for data analysis. 
    merged_gw.to_csv("data/2023-2024/merged_gw.csv", index = False)