import json, csv, os, pathlib
import pandas as pd
import web_scrape as ws
import clean_data as cd

# Check if this seasons data is already saved as a .csv file in the local drive. 
file_path = os.path.abspath("data/2023-2024/team_data.csv")

if os.path.exists(file_path):
    print("File located.\nLoading database from local drive")
    team_df = pd.read_csv(file_path)
else:
    print("File Not Found on Local Machine.\nRetrieving Data From FPL Database.\nSaving database to .csv on local drive")
    ws.update_bootstrap_data()
    team_df = pd.read_csv(file_path)

