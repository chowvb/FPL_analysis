from player_analysis import gw_stats
import pandas as pd

player_involvement = pd.DataFrame({"gw": [],
                                   "team_goals":[],
                                   "player_involvement":[],})


df = gw_stats(308)
team_goals = 0
goal_involvement = 0

for i, home in enumerate(df["was_home"]):
    print(i, home)
    goal_involvement += (df["goals_scored"][i] + df["assists"][i])

    if home == True:
        team_goals += df["team_h_score"][i]
        
    else:
        team_goals += df["team_a_score"][i]

    weekly_stats = pd.DataFrame({"gw": (i+1),
                                 "team_goals": team_goals,
                                 "player_involvement": goal_involvement}, index=[0])

    player_involvement = pd.concat([player_involvement, weekly_stats])