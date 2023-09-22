import team_analysis as ta
import player_analysis as pa
import pandas as pd
import utility
from IPython.display import display
from data_visualisation_tools import get_team_strength_stats

# Select the team name and id number.
team_name = "Liverpool"
team_id = 11

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
display(player_df.head(6))
get_team_strength_stats(team_name, opponent_team)
