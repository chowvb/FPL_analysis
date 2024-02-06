import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

"""
Gets a players historic FPL price/goals/assists per season in the Premier League. 
The player name inputted must be a complete match to the player name in the FPL database 
    ***Note***
    Some of the player names in FPL are the players fullname (E.g., Brazilian players will usually play under an alias rather than their actual name).
    A fix to replace these names to match the player names from the website fbref.

An example of the output of FPL_history() can be found in /images/player_performance_example.png
"""
def FPL_history(player_name):
    # Define the list of historical fpl data that contains player names.
    season_list = ["2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]
    player_name = player_name
    #player_name = "Mohamed Salah"

    # Create a player profile to store each of the seasonal data into. This will be used to produce the final graph/figure
    player_profile_season = pd.DataFrame({
        "name": [],
        "season": [],
        "value":[],
        "goals_scored": [],
        "assists": [],
        "total_points": []
    })


    print(player_name)
    
    # Loop through each of the season in the season list defined at the start of the function
    for season in season_list:
        
        # Read all of the gameweek data
        gw_df = pd.read_csv("data/" + season + "/merged_gw.csv", encoding= "latin-1") # inputting the different seasons as the loop progresses
        gw_df = gw_df[gw_df["name"] == player_name] # Filter the gameweek dataframe to only show the desired.
        gw_df["value"] = (gw_df["value"] / 10) # Divide the value by 10 to match the same value as the fpl website. 
        gw_df = gw_df[["name", "round", "goals_scored", "assists", "total_points", "value"]] # Further filter the dataframe to only include the variables wanted in player_profile.
        gw_df["season"] = season # Add the season as a column
        gw_df.fillna(0) # Replace any N/A values with a zero.
        
        # Try and average the value of the player over the gameweek (FPL will often change the player value throughout the season dependent on the players performance)
        try:
            avg_value = mean(gw_df["value"])
        except:
            avg_value = 0

        # Create a dataframe that stores the season-by-season data
        season_stats_df = pd.DataFrame({
            "name": player_name,
            "season": season,
            "value": avg_value,
            "goals_scored": sum(gw_df["goals_scored"]),
            "assists": sum(gw_df["assists"]),
            "total_points": sum(gw_df["total_points"])
        }, index =[0])

        # Concat seasons_stats_df to the player_profile_season. The new dataframe will show the player stats for each of the seasons in season_list list. 
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
