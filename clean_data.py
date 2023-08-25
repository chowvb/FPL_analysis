import csv, requests, json
import pandas as pd
import numpy as np 
import os
import utility
def scrape_data():
    # Create a dictionary of the position of the players in the raw format and the corrosponding position that that the players play in. 
    position_replace_dict = { 1: "GLK", 2: "DEF", 3 : "MID", 4: "FWD"}   
    
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
    cleaned_players_df = players_df[["first_name", "second_name", "goals_scored", "assists", "total_points",
                                "minutes", "goals_conceded", "creativity", "influence", "threat", "bonus",
                                "bps", "ict_index", "clean_sheets", "red_cards", "yellow_cards", "selected_by_percent",
                                "now_cost", "element_type"]]

    # Replace element_type numbers with corresponding positions
    cleaned_players_df["element_type"].replace(position_replace_dict, inplace = True)

    # Save the cleaned_players_df to a .csv file for offline analysis
    cleaned_players_df.to_csv("data/2023-2024/cleaned_players.csv", index = False)


def get_gw_data(player_id):
        player_id_list = pd.read_csv("data/2023-2024/player_idlist.csv")
        url = "https://fantasy.premierleague.com/api/"
        endpoint = "element-summary/"

        response = requests.get(url + endpoint+ str(player_id)+ "/").json()

        df = pd.DataFrame(response["history"])

        player_id = player_id_list[player_id_list["id"] == int(player_id)].reset_index()

        # Obtain the player name
        player_first_name = player_id.at[0,"first_name"]
        player_second_name = player_id.at[0,"second_name"]

        player_name = player_first_name + " " + player_second_name
        team_name = player_id.at[0,"team"]

        df["element"] = player_name
        df.rename(columns={"element":"name"}, inplace=True)
        df["team"] = team_name
        return df 


def get_extended_gw_data(player_id, GW_number):
        # Define the endpoint to be used
        url = "https://fantasy.premierleague.com/api/"
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


def get_all_gw_data():
    # Load player_idlist.csv
    player_id_list = pd.read_csv("data/2023-2024/player_idlist.csv")
    merged_gw = pd.DataFrame()

    for i, id in enumerate(player_id_list["id"]):
        print("Loading Player: "+ str(i) + "/" + str(len(player_id_list)-1))
        df = get_gw_data(id)

        merged_gw = pd.concat([merged_gw, df])
    
    merged_gw.to_csv("data/2023-2024/merged_gw.csv", index = False)

    
def format_historical_csv():
    season_list = ["2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]
    for season in season_list:
        df = pd.read_csv("data/" + season + "/merged_gw.csv", encoding="latin-1")
        df["name"].replace("_", " ", regex=True, inplace= True)
        df["name"].replace("\d", "", regex= True, inplace=True)
        df["name"] = df["name"].str.rstrip(" ")
        df.to_csv("data/" + season + "/merged_gw.csv", index=False)