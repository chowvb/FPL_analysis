import csv, requests, json
import pandas as pd
import numpy as np 
import os
import utility

""""""
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

""""""
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

        # Return the DataFrame back to the user.
        return df 

""""""
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

""""""
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

""""""    
def format_historical_csv():
    # Define the subdirectories within "/data/" that contain merged_gw.csv files. This list will be iterated through
    season_list = ["2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]

    # Iterate through the seasons list 
    for season in season_list:

        # Read the merged_gw.csv file as a DataFrame
        df = pd.read_csv("data/" + season + "/merged_gw.csv", encoding="latin-1")

        # Replace the format of the names from "_" to " " this is done to remain consistant with the names of players in recent season's merged_gw
        df["name"].replace("_", " ", regex=True, inplace= True)

        # Replace and extra digits that are attached to the players names 
        df["name"].replace("\d", "", regex= True, inplace=True)

        # Replace additional spaces that are the remainder of removing the digits from the names 
        df["name"] = df["name"].str.rstrip(" ")

        # Resave the Dataframe to the same location as it was opened replacing the old file. 
        df.to_csv("data/" + season + "/merged_gw.csv", index=False)