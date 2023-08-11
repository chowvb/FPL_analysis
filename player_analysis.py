import json, requests
import pandas as pd 

def get_basic_stats_GLK():

    # Filter the players DataFrame by position only showing the players with the GLK label. 
    # The DataFrame does require the user to have previously cleaned the data (Converted the player_element to position and from numbers to poition)
    GLK_df = players_df[players_df["Position"] == "GLK"]

    # Create a list with the relavent stats for the goalkeeper position. Futher stats columns can be included by appending the list below
    GLK_stats = ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists", "clean_sheets", "goals_conceded", "saves"]
    
    # Using the GLK_stats list futher filter the GLK_df down so that it only shows the relavent stats columns.
    GLK_df = GLK_df[GLK_stats]
    return GLK_df


def get_basic_stats_DEF():

    # Filter 
    DEF_df = players_df[players_df["Position"] == "DEF"] 
    DEF_stats = ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists", "clean_sheets", "goals_conceded"]
    return DEF_df


def get_basic_stats_MID():
    MID_df = players_df[players_df["Position"] == "MID"] 
    MID_stats = ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists"]
    return MID_df


def get_basic_stats_FWD():
    FWD_df = players_df[players_df["Position"] == "FWD"] 
    FWD_stats ["Name", "id", "Position", "total_points", "bonus", "goals_scored", "assists"]
    return FWD_df

"""
player economy function contains a series of simple equations that calculates the effectiveness of players based on the number of points 
that they score compared to other parameters.

Function input variables:
    1) total_points -> total number of points that a player has collated, input should be taken from the player_stats DataFrame or the .csv file for offline analysis.
    2) minutes_played -> total minutes played for the player selected, (personally a better representation of how well players perform as some players will play lots of matches in a season as last minute substitutions)
    3) now_cost -> how much the player currently costs as this can fluctuate during the season due to performance, this variable shouble be taken from the most recent version of the DataFrame.

Notes:  
"""
def player_economy(total_points, minutes_played, now_cost, goals_scored, assists):
    
    # ppm_economy (points per minute) calculates the average number of points that a player will score per the amount of time they play
    ppm_economy = int(total_points)/int(minutes_played)

    # ppc_economy (point per cost) divide minutes played by 10 to create the same format as FPL website. 
    ppc_economy = total_points/(now_cost/10)

    # mpg_economy (minutes per goal) 
    mpg_economy = goals_scored/minutes_played
    
    # mpa_economy (minutes per assist)
    mpa_economy = assists/minutes_played
