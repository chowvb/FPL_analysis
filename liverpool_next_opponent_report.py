"""
***Following the conclusion of the Premier League Season 2023/2024 this script is now depricated***
"""
import team_analysis as ta
import player_analysis as pa
import pandas as pd
import utility
from IPython.display import display
from data_visualisation_tools import get_team_strength_stats
import numpy as np
import matplotlib.pyplot as plt

"""
***Notes***

Script function - 
    - Updates fpl player data
    - Updates fbref statistics for team data
    
    - Gets Liverpools Next Opponent
    - Gets recent premier league matches between Liverpool and their next opponent. Uses historical FPL datasets.
    - Displays top 5 players based on form as "ones to watch" (Both teams players are included)
    - Spider plot displaying team strengths (Attack/Defence ratings made by fpl)
    - Displays the difficulty level of the next fixture 1-5 (1 = Easy / 5 = Difficult)
    
    - Using fbrefs statistics. Head-to-head stats are generated.

Requires internet connection as functions used within this script requires scraping tables of fbref.com and requesting data from the fpl endpoint.
"""
# Select the team name and id number.
team_name = "Liverpool"
team_id = 11

# Update fbref_data/team_data/ files before reading them.
from fbref_scrape import update_team_statistics

# Use a try statement to update local data files. 
try:
    update_team_statistics() # Update all file names for most recent stats. This funciton scrapes data from fbref.com website

    # request the full fixture list for premier league mathes using get_fixture_list from fixtures python file 
    fixture_list = utility.get_fixture_list() # Fixture list is taken from Fantasy Premier League Database

except Exception: # If there is an error eg., No internet connection, script will continue with data stored locally on machine.
    # Print error statement
    print("There was an error requesting data. System using local data storage")
    
    # Read previous fixture list data
    fixture_list = pd.read_csv("data/2023-2024/fixtures.csv")

    # Continue with the code in the rest of the script.
    pass

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
        team_fixtures = team_fixtures.drop(i) # drop(i) removes the row that contains a value.
    else:
        pass # Skip the rows that contain N/A values in them for remaining fixtures

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
#display(h2h_results) # Print/Display the table of recent results between the two teams 

# Save h2h_results df as a png image to put onto GitHub page.
fig, ax = plt.subplots(figsize=(4,4))
ax.axis("off")
table = ax.table(cellText=h2h_results.values, colLabels=h2h_results.columns, cellLoc = "center", loc= "center", colColours=["#f5f5f5"]*h2h_results.shape[1])
table.auto_set_column_width(range(0, len(h2h_results.columns)))
fig.tight_layout()
plt.savefig("images/h2h_results.png", dpi = 50, bbox_inches = "tight")

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
#display(player_df.head(5))
one_2_watch = player_df.head(5)
fig, ax = plt.subplots(figsize=(4,4))
ax.axis("off")
table = ax.table(cellText=one_2_watch.values, colLabels=one_2_watch.columns, cellLoc = "center", loc= "center", colColours=["#f5f5f5"]*one_2_watch.shape[1])
table.auto_set_column_width(range(0, len(one_2_watch.columns)))
fig.tight_layout()
plt.savefig("images/one_2_watch.png", dpi = 50, bbox_inches = "tight")


# Show fpl team strength statistics by calling the get_team_strength_stats from data_visualiation.py
#get_team_strength_stats(team_name, opponent_team)


csv_df = pd.read_csv("fbref_data/team_data/general_stats.csv", header = [0,1], index_col= 0) # Read general stats .csv file
fbref_team_df = pd.read_csv("fbref_data/team_data/team_id.csv") # Read the team_id.csv

# Filter fbref_team_df the for the desired team to get the team name on fbref (Some team names have subtle differences)
fbref_team_name = fbref_team_df[fbref_team_df["fpl_team"] == team_name].reset_index(drop = True).at[0, "Team"]

# Filter for the fbref team name for the opponent team named from earlier in the script.
fbref_opponent_team_name = fbref_team_df[fbref_team_df["fpl_team"] == opponent_team].reset_index(drop = True).at[0, "Team"]

general_stats_df = csv_df.drop(columns=["Playing Time", "Per 90 Minutes"]).droplevel(0, axis = 1) # Drop the unwanted columns and drop the first column index level. (Theres two levels by default when scraping fbref)

# Read goalkeeper stats from goalkeeping.csv file
gk_df = pd.read_csv("fbref_data/team_data/goalkeeping.csv", header = [0,1], index_col= 0)
filtered_gk_df = gk_df[[("Unnamed: 0_level_0", "Squad"), ("Performance" , "CS")]] # Extract wanted statistics from gk_df and store into filtered_gk_df
filtered_gk_df = filtered_gk_df.droplevel(0, axis = 1) # Drop the first column index (It is no longer required)
filtered_gk_df = filtered_gk_df.loc[filtered_gk_df["Squad"].isin([fbref_team_name, fbref_opponent_team_name])].reset_index(drop = True) # Further filter the dataframe to only include records that contain the team_name and opponent_team (name)

h2h_season_stats = general_stats_df[["Squad", "Age","Poss", "xG", "Gls","xAG", "Ast", "CrdY", "CrdR"]] # Query the general_stats_df for the desired stats
h2h_season_stats = h2h_season_stats.loc[h2h_season_stats["Squad"].isin([fbref_team_name, fbref_opponent_team_name])] # Query again to only get the team_name and opponent_team_name

h2h_season_stats = pd.merge(h2h_season_stats, filtered_gk_df, on = "Squad") # Merge the filtered_gk_df onto the h2h_season_stats (General stats)

# Repeat the previous step for all of the other .csv file found in fbref_data/team_data/
shooting_csv = pd.read_csv("fbref_data/team_data/shooting.csv", header = [0,1], index_col= 0) # Read dataframe from csv file.
shooting_csv = shooting_csv.droplevel(0, axis = 1)
shooting_csv = shooting_csv.loc[shooting_csv["Squad"].isin([fbref_team_name, fbref_opponent_team_name])].reset_index(drop = True) # filter for queried teams (Uses a boolian (mask) for this queries. However, .isin() is probably an easier method of going this.)
shooting_df = shooting_csv[["Squad", "Sh", "SoT", 
                            "SoT%","npxG/Sh"]] # Filter query for stats to be extracted. 
h2h_season_stats = pd.merge(h2h_season_stats, shooting_df, on = "Squad")

passing_df = pd.read_csv("fbref_data/team_data/passing.csv", header = [0,1], index_col = 0) # Read csv file into DataFrame 
filtered_passing_df = passing_df[[("Unnamed: 0_level_0", "Squad"), ("Total", "Cmp%"), ("Unnamed: 21_level_0", "KP")]] # Filter Dataframe for wanted values
filtered_passing_df = filtered_passing_df.droplevel(0, axis = 1) # Drop the first index level.
filtered_passing_df = filtered_passing_df.loc[filtered_passing_df["Squad"].isin([fbref_team_name,fbref_opponent_team_name])].reset_index(drop = True) # Filter the DataFrame to only contain the stats for the two queried teams.

h2h_season_stats = pd.merge(h2h_season_stats, filtered_passing_df, on = "Squad")

# Create a dataframe called summary stats where h2h_season_stats are transposed for the "Squad" allowing for easier comparison between the two clubs.
summary_stats = h2h_season_stats.T.rename(columns= h2h_season_stats["Squad"])
summary_stats = summary_stats.tail(-1)
#display(summary_stats)

# Summary Statistics: generates a dataframe that contains the key stats for each team. 
summary_stats.reset_index(inplace =True)
fig, ax = plt.subplots(figsize=(4,4))
ax.axis("off")
table = ax.table(cellText=summary_stats.values, colLabels=summary_stats.columns, cellLoc = "center", loc= "center", colColours=["#f5f5f5"]*summary_stats.shape[1])
table.auto_set_column_width(range(0, len(summary_stats.columns)))
fig.tight_layout()
plt.savefig("images/summary_stats.png", dpi = 50, bbox_inches = "tight")

from data_visualisation_tools import attacking_radar_plot

# Call and make a radar plot for the two teams comparing attacking stats to the opponent team as well as the league average.
attacking_radar_plot(fbref_team_name, fbref_opponent_team_name)

import data_clean

creativity = data_clean.creativity_GCA
creativity = creativity.loc[creativity["Squad"].isin([team_name, opponent_team])]

defence_tackles = data_clean.defence_tackles
from data_visualisation_tools import radar_plot
radar_plot(defence_tackles, team_name, opponent_team)