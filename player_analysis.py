import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def summary_att_stats():
    gw_data = pd.read_csv("data/2023-2024/players_raw.csv")
    gw_data_goals = gw_data[["web_name", "minutes", 'goals_scored',
       'assists', 'clean_sheets', 'goals_conceded', 'own_goals',
       'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards',
       'saves', 'expected_goals', 'expected_assists',
       'expected_goal_involvements', 'expected_goals_conceded']].sort_values(by="goals_scored", ascending=False)
    
    gw_data_goals = gw_data_goals.head(15).reset_index()
    # Create a scatter plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='expected_goals', y='goals_scored', data=gw_data_goals, hue='web_name', legend=False, s=100)

    # Add labels and title
    plt.xlabel('Expected Goals (xG)')
    plt.ylabel('Goals Scored')
    plt.title('xG vs Goals Scored for Football Players')

    # Add player labels
    for i, player in enumerate(gw_data_goals['web_name']):
        plt.annotate(player, (gw_data_goals['expected_goals'][i], gw_data_goals['goals_scored'][i]), fontsize=12, rotation = 90)

    # Show the plot
    plt.grid(True)
    plt.savefig("images/G_vs_xG_fpl.png", dpi = 300, bbox_inches = "tight")
    plt.show()
    
    gw_data_assists = gw_data.sort_values(by = "assists", ascending=False)
    gw_data_assists = gw_data_assists.head(15).reset_index()
    # Create a scatter plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='expected_assists', y='assists', data=gw_data_assists, hue='web_name', legend=False, s=100)

    # Add labels and title
    plt.xlabel('Expected Assists (xA)')
    plt.ylabel('Assists')
    plt.title('xA vs Assists for Football Players')

    # Add player labels
    for i, player in enumerate(gw_data_assists['web_name']):
        plt.annotate(player, (gw_data_assists['expected_assists'][i], gw_data_assists['assists'][i]), fontsize=12, rotation = 90)

    # Show the plot
    plt.grid(True)
    plt.savefig("images/A_vs_xA_fpl.png", dpi = 300, bbox_inches = "tight")
    plt.show()



    goal_contribution = []
    x_g_contribution = []
    for i, player in enumerate(gw_data["web_name"]):
        goal_contribution.append(gw_data["goals_scored"][i] + gw_data["assists"][i])
        x_g_contribution.append(gw_data["expected_goals"][i] + gw_data["expected_assists"][i])

    gw_data["goal_contribution"] = goal_contribution
    gw_data["expected_goal_contribution"] = x_g_contribution

    gw_data_gc = gw_data[["web_name", "expected_goal_contribution", "goal_contribution"]]
    gw_data_gc = gw_data_gc.sort_values(by = "goal_contribution", ascending= False)
    gw_data_gc = gw_data_gc.head(10).reset_index()
    # Create a scatter plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='expected_goal_contribution', y='goal_contribution', data=gw_data_gc, hue='web_name', legend=False, s=100)

    # Add labels and title
    plt.xlabel('Expected Goal Contributions')
    plt.ylabel('Goal Contributions')
    plt.title('Expected Goals Contributed by Players Against Actual Goal Contributions')

    # Add player labels
    for i, player in enumerate(gw_data_gc['web_name']):
        plt.annotate(player, (gw_data_gc['expected_goal_contribution'][i], gw_data_gc['goal_contribution'][i]), fontsize=12, rotation = 45)

    # Show the plot
    plt.grid(True)
    # Save the plot
    plt.savefig("images/Attacking_Performance.png", dpi = 300, bbox_inches = "tight")
    plt.show()

def points_per_90():
    players_df = pd.read_csv("data/2023-2024/players_raw.csv")
    variables = ["web_name", "element_type", "total_points", "minutes"]
    players_df = players_df[variables]
    ppm = []
    for i, player_name in enumerate(players_df["web_name"]):
        if players_df["minutes"][i] > 0:
            ppm.append(int(players_df["total_points"][i]) / 90)
        else:
            ppm.append(0)
    
    players_df["points_per_90"] = ppm
    players_df.sort_values(by="points_per_90", ascending= False)
    return players_df

