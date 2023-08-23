import requests, json
import pandas as pd
from pprint import pprint
URL = "https://fantasy.premierleague.com/api/fixtures/"

fixtures_json = requests.get(URL).json()
fixtures_df = pd.DataFrame(fixtures_json, index = False)

team_replace_dict = { 
        1 : "Arsenal",
        2 : "Aston Villa",
        3 : "Bournemouth",
        4 : "Brentford",
        5 : "Bighton",
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

fixtures_df["team_a"].replace(team_replace_dict, inplace = True)
fixtures_df["team_h"].replace(team_replace_dict, inplace = True)

df_columns = {
    "current_name": ["id","team_h", "team_h_score", "team_a_score", "team_a", "event", "kickoff_time","stats"],
    "new_name": ["Match_ID","Home", "Home_goals", "Away_goals", "Away", "GW", "kickoff_time", "Match_stats"]
}
def test_function(current_column_name, new_column_name, column_position):
        reorder_col = fixtures_df.pop(current_column_name)
        fixtures_df.insert(column_position, new_column_name, reorder_col)
    
for i in range(len(df_columns["new_name"])):
    test_function(
        df_columns["current_name"][i],
        df_columns["new_name"][i],
        i
        )

fixtures_df = fixtures_df[df_columns["new_name"]].sort_values(by="GW", ascending=True)
