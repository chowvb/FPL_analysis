import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

def FPL_history(player_name):
    season_list = ["2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]
    player_name = player_name
    #player_name = "Mohamed Salah"

    player_profile = pd.DataFrame({
        "name": [],
        "season": [],
        "round": [],
        "value": [],
        "goals_scored": [],
        "assists": [],
        "total_points": []
    })

    player_profile_season = pd.DataFrame({
        "name": [],
        "season": [],
        "value":[],
        "goals_scored": [],
        "assists": [],
        "total_points": []
    })


    print(player_name)
    for season in season_list:
        
        gw_df = pd.read_csv("data/" + season + "/merged_gw.csv", encoding= "latin-1")
        gw_df = gw_df[gw_df["name"] == player_name]
        gw_df["value"] = (gw_df["value"] / 10)
        gw_df = gw_df[["name", "round", "goals_scored", "assists", "total_points", "value"]]
        gw_df["season"] = season
        gw_df.fillna(0)
        
        try:
            avg_value = mean(gw_df["value"])
        except:
            avg_value = 0

        season_stats_df = pd.DataFrame({
            "name": player_name,
            "season": season,
            "value": avg_value,
            "goals_scored": sum(gw_df["goals_scored"]),
            "assists": sum(gw_df["assists"]),
            "total_points": sum(gw_df["total_points"])
        }, index =[0])

        player_profile = pd.concat([player_profile, gw_df])
        player_profile_season = pd.concat([player_profile_season, season_stats_df])
    
    plt.figure(figsize= (10, 6))
    plt.plot(player_profile_season["season"], player_profile_season["goals_scored"], marker = "o", color = "b", linewidth = 2, label = "Goals")
    plt.plot(player_profile_season["season"], player_profile_season["assists"], marker = "^",linestyle = "--",  color = "g", linewidth = 2 , label = "Assists")
    plt.plot(player_profile_season["season"], player_profile_season["value"], marker = "x",linestyle = "-",  color = "r", linewidth = 2 , label = "Value")

    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.title('Player Performance per Season: ' + player_name , fontsize=14)
    plt.legend()

    # Customize grid appearance
    plt.grid(True, linestyle='--', alpha=0.7)

    # Adding shadow to the plot area
    plt.gca().patch.set_facecolor('0.95')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Adding a background grid pattern
    plt.gca().set_axisbelow(True)

    # Adding horizontal lines for reference
    plt.axhline(y=0, color='black', linewidth=0.8, alpha=0.7)

    # Show plot with improved layout
    plt.tight_layout()
    #plt.savefig("player_performance_example.png", dpi = 300, bbox_inches = "tight")
    # Display the plot
    plt.show()