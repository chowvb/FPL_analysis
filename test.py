"""
Spider plot comparing a teams attacking stats against an opponent team or the league average.
Data for this will be supplied by FBref (tables stored in .csv files on the local drive)
Variables to be compared:
    - Goals per game (Gls per 90 - general_stats.csv)
    - Expected Goals per game (xg per 90 - general_stats.csv)
    - Shots per game (Sh/90 - shooting.csv)
    - Shots on target ratio (%) (SoT% - shooting.csv)
    - Dribbles per game (Take-ons -> Attempts - possession.csv)
    - Crosses (Crs - other.csv) 
    - Pass completion (Total -> Comp% - passing.csv)
    - Fouls Against per Game (Performance -> Fld drawn - other.csv)
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from fbref_scrape import update_team_statistics

#update_team_statistics()

general_df = pd.read_csv("fbref_data/team_data/general_stats.csv", header= [0,1], index_col= 0)
shooting_df = pd.read_csv("fbref_data/team_data/shooting.csv", header = [0,1], index_col= 0)
passing_df = pd.read_csv("fbref_data/team_data/passing.csv", header = [0,1], index_col= 0)
other_df = pd.read_csv("fbref_data/team_data/other.csv", header = [0, 1], index_col= 0)
possession_df = pd.read_csv("fbref_data/team_data/possession.csv", header = [0,1], index_col= 0)

#attacking_df = 