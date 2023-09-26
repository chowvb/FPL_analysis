import team_analysis as ta
import player_analysis as pa
import pandas as pd
import utility
from IPython.display import display
from data_visualisation_tools import get_team_strength_stats
import numpy as np


# Select the team name and id number.
team_name = "Liverpool"
team_id = 11

# Update fbref_data/team_data/ files before reading them.
from fbref_scrape import update_team_statistics
update_team_statistics() # Update all file names for most recent stats.

# request the full fixture list for premier league mathes using get_fixture_list from fixtures python file 
fixture_list = utility.get_fixture_list()
# Create two new dataframes which store the fixtures that contain the team_name where they are either home or away.
team_fixtures_h = fixture_list[fixture_list["Home"] == team_name]
team_fixtures_a = fixture_list[fixture_list["Away"] == team_name]
# Concatinate the two dataframes together.
team_fixtures = pd.concat([team_fixtures_h,team_fixtures_a])
# Reorder the data by the game week number so that the fixtures are in cronological order.
team_fixtures = team_fixtures.sort_values(by= "GW", ascending= True).reset_index(drop=True)

# ennumerate through the "Home_goals" and drop the fixtures that have already been played
for i, value in enumerate(team_fixtures["Home_goals"]):
    if pd.notna(team_fixtures.at[i, "Home_goals"]):
        team_fixtures = team_fixtures.drop(i)
    else:
        pass

# Reset the index values 
team_fixtures= team_fixtures.reset_index(drop = True)

# Check whether the team_name is home or away and extract the opponents difficulty 
if team_fixtures.at[0, "Home"] == team_name: # Check if the team playing at home is the desired team 
    opponent_team = team_fixtures.at[0, "Away"] # if true then save the away team as the opposition
    location = "Home" # State that the desired team is playing at home
    next_match_difficulty = team_fixtures.at[0, "team_h_difficulty"] # Obtain the opposition difficulty 
else: # Desired team is not in the "home" field
    opponent_team = team_fixtures.at[0, "Home"] # select the team that is playing at home as the opposition team 
    location = "Away" # Desired team will be playing away from home 
    next_match_difficulty = team_fixtures.at[0, "team_a_difficulty"] # obtain the opposition difficulty 

# Print who the next match is against and whether its home/away. When the match is to be scheduled. Print the difficulty rating of the oppositon team. 
print("Next match is " + location + " against " + opponent_team + "\nOn: " + team_fixtures.at[0,"kickoff_time"] + "\nDifficulty rating: " + str(next_match_difficulty) + "/5\n")

# Using h2h_results from team_analysis.py obtain historical fixtures between team_name and opposition_team
h2h_results = ta.h2h_results(team= team_name, opp_team= opponent_team)

print("Recent results in the Premier League ") #Print a statement
display(h2h_results) # Print/Display the table of recent results between the two teams 

print("\n\nOnes To Watch") 
player_database = pd.read_csv("data/2023-2024/players_raw.csv") # Open the players database 
team_id = pd.DataFrame(utility.team_replace_dict2) # create a dataframe of the teams/team_id
selected_team = team_id[team_id["Team"] == team_name].reset_index(drop = True) # Filter for the desired team
opp_team = team_id[team_id["Team"] == opponent_team].reset_index(drop = True) # Filter for the opposition team
selected_team_players = player_database[player_database["team"] == selected_team.at[0, "team_id"]]
opposition_team_players = player_database[player_database["team"] == opp_team.at[0, "team_id"]]
player_df = pd.concat([selected_team_players, opposition_team_players]) # Combine the two databases for players from both teams
player_df = player_df.sort_values(by = "form", ascending= False) # Reorder the dataframe based on "form" 
player_df = player_df[["web_name", "total_points", "goals_scored", "assists", "form"]] # Filter the fields to be shown to display the most important variables.

# Print the top 5 players based off form.
display(player_df.head(5))
get_team_strength_stats(team_name, opponent_team)


# Current Seasons Stats General stats
csv_df = pd.read_csv("fbref_data/team_data/general_stats.csv", header = [0,1], index_col= 0)

# Load the team names and endpoints for premier league teams.
fbref_team_df = pd.read_csv("fbref_data/team_data/team_id.csv")

# Filter to get the team name for both the wanted team (Liverpool) and their next opponents
fbref_team_name = fbref_team_df[fbref_team_df["fpl_team"] == team_name].reset_index(drop = True).at[0, "Team"]
fbref_opp_team_name = fbref_team_df[fbref_team_df["fpl_team"] == opponent_team].reset_index(drop = True).at[0, "Team"]

# Drop the columns playing time and per 90 minuts stats from the multi-index columns. Then drop the first index level. 
expected_df = csv_df.drop(columns=["Playing Time", "Per 90 Minutes"]).droplevel(0, axis = 1)

# Create a boulian that contains the names for both teams
mask = (expected_df["Squad"] == fbref_team_name) | (expected_df["Squad"] == fbref_opp_team_name)

# Filter expected_df for Summary stats.
h2h_season_stats = expected_df[["Squad", "Age","Poss", "xG", "Gls","xAG", "Ast", "CrdY", "CrdR"]]

h2h_season_stats = h2h_season_stats[mask].transpose().drop("Squad", axis = 0) # Transpose the axis so that the two team names are the columns and the row indexes are the comparison variables. 
h2h_season_stats.columns = [team_name, opponent_team] # Rename the column names post dataframe transpose to the two team names. (Desired team first follwed by opposition team)
h2h_season_stats = h2h_season_stats.rename(index = {"Age": "Avg Age",
                                                    "Poss": "Avg Possession",
                                                    "Gls": "Goals",
                                                    "Ast": "Assists",
                                                    "CrdY": "Yellow Cards",
                                                    "CrdR": "Red Cards"
                                                    })


# Read goalkeeper stats from goalkeeping.csv file
gk_df = pd.read_csv("fbref_data/team_data/goalkeeping.csv", header = [0,1], index_col= 0) # header [0,1] reads the dataframe as a multi-index column.
filtered_gk_df = gk_df[[("Unnamed: 0_level_0", "Squad"), ("Performance" , "CS")]] # Extract wanted statistics from gk_df and store into filtered_gk_df
filtered_gk_df = filtered_gk_df.droplevel(0, axis = 1) # Drop the first column index (It is no longer required)
filtered_gk_df = filtered_gk_df.loc[filtered_gk_df["Squad"].isin([fbref_team_name, fbref_opp_team_name])].reset_index(drop = True) # Further filter the dataframe to only include records that contain the team_name and opponent_team (name)
filtered_gk_df = filtered_gk_df.transpose().drop("Squad", axis = 0) # transpose the dataframe and drop the "Squad" row.
filtered_gk_df.columns = [team_name, opponent_team] # Rename the columns to team names 
filtered_gk_df = filtered_gk_df.rename(index= {"CS": "Clean Sheets"}) # rename the row indexs for cleaner viewing when printed/displayed
h2h_season_stats = pd.concat([h2h_season_stats, filtered_gk_df], axis = 0) # Concatinate dataframe to the main h2h_season_stats dataframe by concating to rows rather than columns.

# Read the shooting stats from shooting.csv. Mostly follows the same logic as the previous stats query for goalkeepers.
shooting_csv = pd.read_csv("fbref_data/team_data/shooting.csv", header = [0,1], index_col= 0) # Read dataframe from csv file.
shooting_csv = shooting_csv[mask].reset_index(drop = True) # filter for queried teams (Uses a boolian (mask) for this queries. However, .isin() is probably an easier method of going this.)
shooting_df = shooting_csv[[("Unnamed: 0_level_0", "Squad"), ("Standard", "Sh"), ("Standard", "SoT"), 
                            ("Standard", "SoT%"), ("Expected", "npxG/Sh")]].droplevel(0, axis = 1) # Filter query for stats to be extracted. 
shooting_df = shooting_df.transpose().drop("Squad", axis = 0) # Transpose and drop the "Squad" row.
shooting_df.columns = [team_name, opponent_team] # Rename the column names to the team names
shooting_df = shooting_df.rename(index = {"Sh" : "Shots",
                                          "SoT": "Shots on Target",
                                          "SoT%": "Shots on Target (%)",
                                          "npxG/Sh": "xG per Shot"
                                          }) # Rename the index names to be easier to understand for casual viewers.
h2h_season_stats = pd.concat([h2h_season_stats, shooting_df], axis=0) # Concat to the h2h_season_stats 

# Adding passing stats to the h2h_season_stats dataframe
passing_df = pd.read_csv("fbref_data/team_data/passing.csv", header = [0,1], index_col = 0) # Read csv file into DataFrame 
filtered_passing_df = passing_df[[("Unnamed: 0_level_0", "Squad"), ("Total", "Cmp%"), ("Unnamed: 21_level_0", "KP")]] # Filter Dataframe for wanted values
filtered_passing_df = filtered_passing_df.droplevel(0, axis = 1) # Drop the first index level.
filtered_passing_df = filtered_passing_df.loc[filtered_passing_df["Squad"].isin([fbref_team_name,fbref_opp_team_name])].reset_index(drop = True) # Filter the DataFrame to only contain the stats for the two queried teams.
filtered_passing_df = filtered_passing_df.transpose().drop("Squad", axis = 0) # Drop the "Squad" row
filtered_passing_df.columns = [team_name, opponent_team] # Rename the columns to the team names. 
filtered_passing_df = filtered_passing_df.rename(index={"Cmp%": "Pass Completion (%)",
                                                        "KP": "Key Passes"}) # Rename the row index names for more readable names.
h2h_season_stats = pd.concat([h2h_season_stats, filtered_passing_df], axis = 0) # Concat filtered DataFrame to the h2h_season_stats 

# Get Total FPL points for each of the two teams. 
from update_fpl_data import scrape_data
scrape_data() # Call scrape_data from update_fpl_data.py to update cleaned_players.csv before reading the dataframe later.
cleaned_player_df = pd.read_csv("data/2023-2024/cleaned_players.csv") # Read csv file as a DataFrame
team_points_df = np.round(cleaned_player_df.groupby("team", as_index = False).aggregate({"total_points" : np.sum}), 2) # group all players by team name and aggregate the total_points scored
h2h_fpl_points_df = team_points_df.loc[team_points_df["team"].isin([team_name, opponent_team])] # Filter the DataFrame for the two queried teams
h2h_fpl_points_df =h2h_fpl_points_df.transpose().drop("team", axis = 0) # transpose and drop the team names("team")
h2h_fpl_points_df.columns = [team_name, opponent_team] # Rename the column headers to the corresponding team names
h2h_fpl_points_df = h2h_fpl_points_df.rename(index = {"total_points" : "FPL Points"}) # Rename in row index names to an easier name to read 
h2h_season_stats = pd.concat([h2h_season_stats, h2h_fpl_points_df], axis = 0) # Concat to h2h_season_stats dataframe.

display(h2h_season_stats) # Display the dataframe
