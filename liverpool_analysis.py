import clean_data as cd
import team_analysis as ta
import player_analysis as pa
import pandas as pd




team_name = "Liverpool"
team_id = 11

def main_function(team_id, team_name):
    player_roster_df = ta.get_player_roster(team_id).reset_index(drop=True)

    primary_df, secondary_df = cd.scrape_and_clean_player_data()

    squad_stats = (primary_df[primary_df["team"] == team_name]).reset_index(drop=True)
    squad_stats = squad_stats.sort_values(by= "total_points", ascending = False)


    economy = {"id": [],
    "economy":[] }

    player_efficiency = {"id": [] ,
    "player_efficiency_goals":[] ,
    "player_efficiency_assists": []}

    player_contributions = {"id":[], 
    "%_goal_involvement": []}

    for player in squad_stats["id"]:
        print(player)
        economy["id"].append(player)
        economy["economy"].append(pa.economy(player))

        player_efficiency["id"].append(player)
        player_efficiency_goals, player_efficiency_assists = pa.player_efficiency(player)
        player_efficiency["player_efficiency_goals"].append(player_efficiency_goals)
        player_efficiency["player_efficiency_assists"].append(player_efficiency_assists)

        player_contributions["id"].append(player)
        player_contributions["%_goal_involvement"].append(pa.player_contribution(player))

    df = pd.DataFrame(economy)
    df = pd.merge(df, pd.DataFrame(player_efficiency), on="id")
    df = pd.merge(df, pd.DataFrame(player_contributions), on = "id")
    summary_df = pd.merge(squad_stats[["id","web_name","team", "position","price", "total_points","goals", "assists"]],df, on="id")
    return summary_df

def full_db_analysis():
    team_id_dict = pd.DataFrame({"id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                            "team": 
                            ["Arsenal",
                                "Aston Villa",
                                "Bournemouth",
                                "Brentford",
                                "Brighton",
                                "Burnley",
                                "Chelsea",
                                "Crystal Palace", 
                                "Everton",
                                "Fulham",
                                "Liverpool",
                                "Luton",
                                "Man City",
                                "Man Utd",
                                "Newcastle",
                                "Nott'm Forrest",
                                "Sheffield Utd",
                                "Spurs",
                                "West Ham",
                                "Wolves"]})

    df1 = pd.DataFrame({"id":[],
                    "web_name":[],
                    "team":[],
                    "position":[],
                    "price": [], 
                    "total_points": [],
                    "goals": [],
                    "assists":[],
                    "economy":[],
                    "player_efficiency_goals":[],
                    "player_efficiency_assists":[],
                    "%_goal_involvement": []
                    })

    for team in range(len(team_id_dict["id"])):
        df1 = pd.concat([df1, main_function(team_id= team_id_dict["id"][team], team_name= team_id_dict["team"][team])], axis=0)

    df1 = df1.fillna(0)
    return df1


# Analyse Liverpool Performance
df = main_function(team_name=team_name, team_id=team_id)
df.fillna(0)
