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