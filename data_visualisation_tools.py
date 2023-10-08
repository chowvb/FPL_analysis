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