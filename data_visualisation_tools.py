import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Creates a spider plot that compares two teams fpl strength thats is created be FPL. 
"""
def get_team_strength_stats(team_name, opponent_name):
    # Load the teams_strength_stat.csv file
    team_strength = pd.read_csv("data/2023-2024/teams_strength_stat.csv", index_col=None)

    def plot_octagon(ax, center, size, team_one, team_two):
        # Calculate the coordinates of the octagon vertices
        angles = np.linspace(0, 2*np.pi, 9)[:-1]
        x = center[0] + size * np.cos(angles)
        y = center[1] + size * np.sin(angles)

        # Create a list for the first team stats
        x2 = []
        y2 = []

        # Create a list for the second team stats
        x3 = []
        y3 = []
        for i in range(len(team_one)):

            x2_score = team_one[i] * np.cos(angles)
            x3_score = team_two[i] * np.cos(angles)
            
            x2.append(x2_score[i])
            x3.append(x3_score[i])

            y2_score = team_one[i] * np.sin(angles)
            y3_score = team_two[i] * np.sin(angles)

            y2.append(y2_score[i])
            y3.append(y3_score[i])
        labels = ["Away_overall", "Away_attack", "Overall_attack", "Home_attack", "Home_overall", "Home_defence", "Overall_defence", "Away_defence"]
        for i, label in enumerate(labels):
            plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0,0), ha='center')
        # Plot the octagon
        ax.fill(x, y, color = "Black", alpha = 0.0)
        ax.fill(x2, y2, color = "Red", alpha = 0.3)
        ax.plot(x2, y2, color = "Red", alpha = 0.3, label = team_name)
        ax.fill(x3, y3, color = "Blue", alpha = 0.3)
        ax.plot(x3, y3, color = "Blue", alpha = 0.3, label = opponent_name)


    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set aspect ratio to equal to make the octagon appear symmetric
    ax.set_aspect('equal', adjustable='datalim')

    # Set plot limits
    ax.set_xlim(-2000, 2000)
    ax.set_ylim(-2000, 2000)

    def get_team_strength(t1, t2):
        t1_scores = team_strength[team_strength["name"] == t1]
        t2_scores = team_strength[team_strength["name"] == t2]
        t1_formatted = t1_scores.drop(t1_scores.columns[0], axis = 1).iloc[0].to_list()
        t2_formatted = t2_scores.drop(t2_scores.columns[0], axis = 1).iloc[0].to_list()
        return t1_formatted, t2_formatted

    t1, t2 =  get_team_strength(team_name, opponent_name)


    # Call the function to plot the octagon
    plot_octagon(ax, center=(0, 0), size=1800, team_one= t1, team_two= t2 )

    # Set axis labels and title
    ax.legend()
    # Show the plot
    plt.axis("off")
    plt.show()

"""
Creates a spider plot comparing a teams attacking statistics to the league average. 
Alternatively compare a teams attacking statistics against an opponent team."""
#def att_stats_comparison():

def attacking_radar_plot(team1, team2):
    import numpy as np 
    import plotly.graph_objects as go

    team1 = team1
    team2 = team2

    # Get the number of matches played (This will be needed when calculating the number of crosses and number of fouls per game a team has)
    pl_table = pd.read_csv("fbref_data/team_data/pl_table.csv", index_col = 0)

    # Read in all the csv files that contain the variables that we want. 
    general_df = pd.read_csv("fbref_data/team_data/general_stats.csv", header = [0,1], index_col= 0)
    shooting_df = pd.read_csv("fbref_data/team_data/shooting.csv", header = [0,1], index_col= 0)
    other_df = pd.read_csv("fbref_data/team_data/other.csv", header = [0, 1], index_col= 0)
    possession_df = pd.read_csv("fbref_data/team_data/possession.csv", header = [0,1], index_col= 0)

    general_df = general_df[[("Unnamed: 0_level_0", "Squad"),("Performance", "Gls"), ("Expected", "xG")]]
    general_df = general_df.droplevel(0, axis = 1)

    attacking_df = general_df

    shooting_df = shooting_df[[("Unnamed: 0_level_0", "Squad"), ("Standard", "Sh/90"), ("Standard", "SoT%")]]
    shooting_df = shooting_df.droplevel(0, axis = 1)
    attacking_df = pd.merge(attacking_df, shooting_df, on = "Squad")

    possession_df = possession_df[[("Unnamed: 0_level_0", "Squad"), ("Take-Ons", "Att")]]
    possession_df = possession_df.droplevel(0, axis = 1)
    possession_df["Dribbles per 90"] = possession_df["Att"] / pl_table["MP"][0]
    possession_df = possession_df.drop(columns= "Att")
    attacking_df = pd.merge(attacking_df, possession_df, on = "Squad")



    other_df = other_df[[("Unnamed: 0_level_0", "Squad"), ("Performance", "Crs"), ("Performance", "Fls")]]
    other_df = other_df.droplevel(0, axis = 1)
    other_df["Crs per 90"] = other_df["Crs"] / pl_table["MP"][0]
    other_df["Fls per 90"] = other_df["Fls"] / pl_table["MP"][0]
    other_df = other_df.drop(columns=["Crs", "Fls"])
    attacking_df = pd.merge(attacking_df, other_df, on = "Squad")

    attacking_df = attacking_df.loc[attacking_df["Squad"].isin([team1,team2])]

    radar_chart_df = attacking_df.loc[attacking_df["Squad"].isin([team1,team2])]
    radar_chart_df = radar_chart_df.T.rename(columns=radar_chart_df["Squad"])
    radar_chart_df = radar_chart_df.tail(-1)

    league_average = attacking_df
    league_average.set_index("Squad", inplace = True)
    league_average_stats = league_average.mean()

    categories = radar_chart_df.index.tolist()
    team1_data = radar_chart_df[team1].values
    team2_data = radar_chart_df[team2].values

    import plotly.graph_objects as go
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = team1_data,
        theta= categories,
        fill = "toself",
        name = team1
    ))
    fig.add_trace(go.Scatterpolar(
        r = team2_data,
        theta= categories,
        fill = "toself",
        name = team2
    ))
    fig.add_trace(go.Scatterpolar(
        r = league_average_stats,
        theta= categories,
        fill = "toself",
        name = "League Average"
    ))
    
    import plotly.io as pio
    fig.show()
    fig.write_image("images/attacking_h2h_radar_chart.png")
    fig.write_html("interactive_plots/attacking_h2h_radar_chart.html")
    return 