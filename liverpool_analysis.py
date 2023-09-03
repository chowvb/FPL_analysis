import clean_data as cd
import team_analysis as ta
import player_analysis as pa
import pandas as pd
from fixtures import get_fixture_list
import utility
from IPython.display import display
from data_visualisation_tools import get_team_strength_stats
team_name = "Liverpool"
team_id = 11


fixture_list = get_fixture_list()
team_fixtures_h = fixture_list[fixture_list["Home"] == team_name]
team_fixtures_a = fixture_list[fixture_list["Away"] == team_name]
team_fixtures = pd.concat([team_fixtures_h,team_fixtures_a])
team_fixtures = team_fixtures.sort_values(by= "GW", ascending= True).reset_index(drop=True)
for i, value in enumerate(team_fixtures["Home_goals"]):
    if pd.notna(team_fixtures.at[i, "Home_goals"]):
        team_fixtures = team_fixtures.drop(i)
    else:
        pass

team_fixtures= team_fixtures.reset_index(drop = True)

if team_fixtures.at[0, "Home"] == team_name:
    opponent_team = team_fixtures.at[0, "Away"]
    location = "Home"
    next_match_difficulty = team_fixtures.at[0, "team_h_difficulty"]
else:
    opponent_team = team_fixtures.at[0, "Home"]
    location = "Away"
    next_match_difficulty = team_fixtures.at[0, "team_a_difficulty"]

print("Next match is " + location + " against " + opponent_team + "\nOn: " + team_fixtures.at[0,"kickoff_time"] + "\nDifficulty rating: " + str(next_match_difficulty) + "/5\n")

h2h_results = ta.h2h_results(team= team_name, opp_team= opponent_team)

print("Recent results in the Premier League ")

display(h2h_results)

print("\n\nOnes To Watch")
player_database = pd.read_csv("data/2023-2024/players_raw.csv")

team_id = pd.DataFrame(utility.team_replace_dict2)
selected_team = team_id[team_id["Team"] == team_name].reset_index(drop = True)
opp_team = team_id[team_id["Team"] == opponent_team].reset_index(drop = True)

selected_team_players = player_database[player_database["team"] == selected_team.at[0, "team_id"]]
opposition_team_players = player_database[player_database["team"] == opp_team.at[0, "team_id"]]

player_df = pd.concat([selected_team_players, opposition_team_players])
player_df = player_df.sort_values(by = "form", ascending= False)
player_df = player_df[["web_name", "total_points", "goals_scored", "assists", "form"]]

display(player_df.head(5))
get_team_strength_stats(team_name, opponent_team)
