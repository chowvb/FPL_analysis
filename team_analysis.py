import pandas as pd
import csv, json, requests


def update_bootstrap_data():
    """
Request current season stats from FPL api.
It then filters the scraped results into display stats regarding teams. 
Saves the database into a .csv file for locally stored data for offline analysis. 
""" 
    # Set the base URL for Fantasy football api
    base_link = "https://fantasy.premierleague.com/api/"

    # Combine the base link above with the extension for the bootstrap-static. 
    bootstrap = requests.get(base_link+"bootstrap-static/").json()

    # Create a DataFrame with the "teams" filter to select teams only data
    team_data = pd.DataFrame(bootstrap["teams"])

    # Save the data to a .csv file for offline work 
    team_data.to_csv("data/2023-2024/team_data.csv")

    # return the stored values to be used in the future. 
    return bootstrap, team_data


# Data for the 2022-2023 season can be pulled from the following GHub Repo https://github.com/vaastav/Fantasy-Premier-League/tree/master/data/2022-23
# Season parameter should be inputted as "20XX-20XX" dependent on the users preference
def clean_team_data(season):

    # Using pandas read the saved dataframe data from the .csv file. The inputted season in the function will dictate which seasons data is cleaned
    team_df = pd.read_csv("data/"+ season + "/team_data.csv")

    # Filter and pull out the relavent strength stats from the team_df into a new DataFrame
    team_strength_stat = team_df[["short_name", "strength_overall_home", "strength_attack_home", "strength_attack_away", "strength_defence_home", "strength_defence_away"]]
    
    # Save the team strength database into a new .csv file
    team_strength_stat.to_csv("data/"+ season + "/teams_strength_stat.csv")
