import requests, json
import pandas as pd
from pprint import pprint
"""
Retrieve fixture list for all 380 fixtures in the premier league season, this fuction returns the list however, there is not much analysis to be done on this. 
"""
# Function to retrieve and clean fixture list data
def get_fixture_list():
    """
    Args:

    Returns:

    Example:
    """
    # Define url endpoint
    URL = "https://fantasy.premierleague.com/api/fixtures/"

    # Request data from FPL
    fixtures_json = requests.get(URL).json()

    # Convert data from json to pandas DataFrame
    fixtures_df = pd.DataFrame(fixtures_json)

    # Define a list to replace team id with the actual name of the clubs
    team_replace_dict = { 
            1 : "Arsenal",
            2 : "Aston Villa",
            3 : "Bournemouth",
            4 : "Brentford",
            5 : "Brighton",
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

    # Using the team_replace_dict replace the numbers corresponding to clubs for both home and away teams 
    fixtures_df["team_a"].replace(team_replace_dict, inplace = True)
    fixtures_df["team_h"].replace(team_replace_dict, inplace = True)

    # Define the columns that we want to keep along with the new name of each of the columns for easier reading
    df_columns = {
        "current_name": ["id","team_h", "team_h_score", "team_a_score", "team_a", "event", "kickoff_time","stats", "team_h_difficulty", "team_a_difficulty"],
        "new_name": ["Match_ID","Home", "Home_goals", "Away_goals", "Away", "GW", "kickoff_time", "Match_stats", "team_h_difficulty", "team_a_difficulty"]
    }

    # Define a function that changes te names of the columns from current names to new names and reorder the dataframe to a more user friendly layout 
    def test_function(current_column_name, new_column_name, column_position):
            reorder_col = fixtures_df.pop(current_column_name)
            fixtures_df.insert(column_position, new_column_name, reorder_col)
    
    # Loop through each of the rows in the DataFrame calling the test funcion each time to replace the column names. 
    for i in range(len(df_columns["new_name"])):
        test_function(
            df_columns["current_name"][i],
            df_columns["new_name"][i],
            i
            )

    # Filter fixtures_df to only contain the columns in df_columns and sort by the game week (GW) 
    fixtures_df = fixtures_df[df_columns["new_name"]].sort_values(by="GW", ascending=True)

    # Return the Data Frame
    return fixtures_df
