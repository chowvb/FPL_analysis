import pandas as pd
import csv, json, requests
import numpy as np
from bs4 import BeautifulSoup

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
    return team_data


# Data for the 2022-2023 season can be pulled from the following GHub Repo https://github.com/vaastav/Fantasy-Premier-League/tree/master/data/2022-23
# Season parameter should be inputted as "20XX-20XX" dependent on the users preference
def clean_team_data(season):

    # Using pandas read the saved dataframe data from the .csv file. The inputted season in the function will dictate which seasons data is cleaned
    team_df = pd.read_csv("data/"+ season + "/team_data.csv")

    # Generate an attacking overall and defending overall stat for each of the teams 
    attack_overall = []
    defence_overall = []

    # Loop through the each of the teams
    for team in range(len(team_df["strength_attack_home"])):

        # Calculate attack strength by averaging home and away scores.
        attack = ((team_df["strength_attack_home"].iloc[team] + team_df["strength_attack_away"].iloc[team]) / 2)

        # Calculate defence strength by averaging home and away scores. 
        defence = ((team_df["strength_defence_home"].iloc[team] + team_df["strength_defence_away"].iloc[team]) / 2)

        # At the end of each loop add the attack score to the scores respective list (round the scores to the nearest integer)
        attack_overall.append(np.round(attack))
        defence_overall.append(np.round(defence))

    # Filter and pull out the relavent strength stats from the team_df into a new DataFrame
    team_strength_stat = team_df[["short_name", "strength_overall_home", "strength_overall_away", "strength_attack_home", "strength_attack_away", "strength_defence_home", "strength_defence_away"]]
    
    # Add the two new lists as new columns in the DataFrame
    team_strength_stat["attack_overall"] = attack_overall
    team_strength_stat["defence_overall"] = defence_overall
    
    # Save the team strength database into a new .csv file
    team_strength_stat.to_csv("data/"+ season + "/teams_strength_stat.csv", index = False)


# Define a function to copy and process the Premier League table from SkySports returns the league table as a DataFrame
def copy_premier_league_table():
    
    # Define the URL of Skysports premier league table
    url = "https://www.skysports.com/premier-league-table"
    
    # Send a HTTP GET request to the provided URL and store the response
    response = requests.get(url)
    
    # Define a dictionary to replace the team names to the FPL names
    team_replace_dict = { 
        "Arsenal" : "Arsenal",
        "Aston Villa" : "Aston Villa",
        "Bournemouth" : "Bournemouth",
        "Brentford" : "Brentford",
        "Brighton and Hove Albion" : "Brighton",
        "Burnley" : "Burnley",
        "Chelsea" : "Chelsea",
        "Crystal Palace" : "Crystal Palace", 
        "Everton" : "Everton",
        "Fulham" : "Fulham",
        "Liverpool" : "Liverpool",
        "Luton Town" : "Luton",
        "Manchester City" : "Man City",
        "Manchester United" : "Man Utd",
        "Newcastle United" : "Newcastle",
        "Nottingham Forrest" : "Nott'm Forrest",
        "Sheffield United" : "Sheffield Utd",
        "Tottenhap Hotspur" : "Spurs",
        "West Ham United" : "West Ham",
        "Wolverhampton Wanderers" : "Wolves"
    }

    # Check if the HTTP response code is 200 (OK)
    if response.status_code == 200:

        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with the relevant class or id
        table = soup.find('table', class_='standing-table__table')
        
        # Check if table element is found
        if table:
            data = [] # Initialise a list to store the table data
            headers = [] # Initialise a list to store the table headers
            
            # Extract header row
            header_row = table.find('thead').find('tr')
            header_columns = header_row.find_all('th')
            headers = [header.get_text(strip=True) for header in header_columns]
            
            # Iterate through rows and extract data and extract the data from the cells
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all(['th', 'td'])
                row_data = [column.get_text(strip=True) for column in columns]
                
                # Skip adding the header row data to the data list
                if row_data != headers:
                    data.append(row_data)
            
            # Convert data into a DataFrame using pandas
            df = pd.DataFrame(data, columns=headers)
            df.dropna(inplace=True)  # Drop rows with missing values
            df.reset_index(drop=True, inplace=True) # Reset row indicies
            
            # Replace team names with FPL names in the "Team" column of the DataFrame
            df["Team"].replace(team_replace_dict, inplace = True)

            # Return the processed DataFrame
            return df
        else:
            print("Table not found on the page.")
    else:
        print("Failed to fetch the webpage.")


def get_player_roster(team_id):

    # Load player_raw.csv
    players_raw_csv = pd.read_csv("data/2023-2024/players_raw.csv")
    player_roster = players_raw_csv[players_raw_csv["team"]== team_id]
    player_roster = player_roster[["first_name", "second_name", "web_name", "id"]]
    return player_roster