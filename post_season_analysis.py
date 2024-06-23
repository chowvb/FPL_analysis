"""
In this file contains all of the data analysis following the conclusion of the Premier League Season 2023/2024"""
import pandas as pd
from utility import team_replace_dict, team_replace_fbref_to_fpl
import data_clean
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Open the .csv file containing player statistics as a dataframe
fpl_player_data = pd.read_csv("data/2023-2024/players_raw.csv")
fpl_player_data["team"].replace(team_replace_dict, inplace= True)

aggregate_functions = {"total_points":"sum", "goals_scored":"sum", "expected_goals":"sum", "assists": "sum", "expected_assists": "sum", "yellow_cards": "sum", "red_cards": "sum"}
team_data = fpl_player_data.groupby(by=["team"]).aggregate(aggregate_functions)

team_data["goal_efficiency"] = team_data["goals_scored"] - team_data["expected_goals"]
team_data["assist_efficiency"] = team_data["assists"] - team_data["expected_assists"]
team_data = team_data.reindex(sorted(team_data.columns), axis=1)
team_data = team_data.reset_index()


"""
This following section we will look at Premier League teams set-piece effectiveness
"""
creativity_GCA_df = data_clean.creativity_GCA
creativity_SCA_df = data_clean.creativity_SCA

creativity_df = creativity_SCA_df
creativity_df = creativity_df.merge(creativity_GCA_df, on = "Squad")
creativity_df["Squad"].replace(team_replace_fbref_to_fpl, inplace = True)

setpieces = creativity_df[["Squad", "PassDead_x", "PassDead_y"]]
setpieces["Efficiency (%)"] = (setpieces["PassDead_y"] / setpieces["PassDead_x"] * 100).round()
setpieces.sort_values("Efficiency (%)", ascending= False)
setpieces = setpieces.set_index("Squad")

# Convert setpieces into a markdown format to be copied and pasted into README.md for GitHub
setpieces_md = tabulate(setpieces, headers= "keys", tablefmt="pipe")
#print(setpieces_md)

"""
In this section will be analysing the passing and build-up play of each of the teams
"""
passing_short_df = data_clean.passing_short
passing_medium_df = data_clean.passing_medium
passing_long_df = data_clean.passing_long

passing_df = data_clean.passing[[["Unnamed: 0_level_0", "Squad"], ["Total", "Att"]]].droplevel(0, axis = 1)
passing_df["Short_Passes_%"] = (passing_short_df["Att"]/passing_df["Att"] * 100).round()
passing_df["Medium_Passes_%"] = (passing_medium_df["Att"]/passing_df["Att"] * 100).round()
passing_df["Long_Passes_%"] = (passing_long_df["Att"]/passing_df["Att"] * 100).round()
passing_df = passing_df.drop(columns = "Att", axis = 1)
passing_df = passing_df.set_index("Squad")

# Convert passing_df into markdown format to be copied and pasted into README.md for GitHub
passing_md = tabulate(passing_df, headers = "keys", tablefmt="pipe")
# print(passing_md)

passing_dist_df = data_clean.passing[[["Unnamed: 0_level_0", "Squad"], ["Total", "Cmp"], ["Total", "TotDist"]]].droplevel(0, axis = 1)
passing_dist_df.sort_values("Average Pass Dist (Y)", ascending = False)