import json, requests, csv 
import pandas as pd

base_link = "https://fantasy.premierleague.com/api/"

# Request current season stats from FPL api
def update_bootstrap_data():
    
    # Combine the base link above with the extension for the bootstrap-static. 
    bootstrap = requests.get(base_link+"bootstrap-static/").json()

    # Create a DataFrame with the "teams" filter to select teams only data
    team_data = pd.DataFrame(bootstrap["teams"])

    # Save the data to a .csv file for offline work 
    team_data.to_csv("data/2023-2024/team_data.csv")

    # return the stored values to be used in the future. 
    return bootstrap, team_data

def update_player_data():

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