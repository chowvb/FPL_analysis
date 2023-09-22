import requests
import pandas as pd
from bs4 import BeautifulSoup


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
        16 : "Nott'm Forest",
        17 : "Sheffield Utd",
        18 : "Spurs",
        19 : "West Ham",
        20 : "Wolves"
    }
team_replace_dict2 = {"team_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                         "Team": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford",
                                "Brighton", "Burnley", "Chelsea", "Crystal Palace", 
                                "Everton", "Fulham", "Liverpool", "Luton", "Man City",
                                "Man Utd", "Newcastle", "Nott'm Forest", "Sheffield Utd",
                                "Spurs", "West Ham","Wolves"]
    }


team_replace_dict_fbref = {"fpl_team_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                         "Team": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford",
                                "Brighton", "Burnley", "Chelsea", "Crystal Palace", 
                                "Everton", "Fulham", "Liverpool", "Luton Town", "Manchester City",
                                "Manchester Utd", "Newcastle Utd", "Nott'm Forest", "Sheffield Utd",
                                "Tottenham", "West Ham","Wolves"]
    }


"""
get_extended_gw_data() - utilises a different URL Endpoint to access gameweek data using the player_id and GW_number as arguments. 

*** Notes***
function is currently redundant as get_gw_data() is a more efficient function to obtain data. Unsure what the differences between the two requests.
 - I will add the differences in the fields that are returned when using this URL endpoint intead of the one used in get_gw_data(). 
 """
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



"""
To be used on set-up to reformat the merged_gw.csv files to match the current formatting of this seasons merged_gw.csv file.
This function was designed to remove a bug from the downloaded data where the player names contained an underscore between the first name and second name. This function removes the underscore and 
any of the characters at the end of the players name. 

*** Note ***
This is a one time function to clean all the merged_gw.csv files and normalize the players names. 
"""    
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


"""
*** Notes ***
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