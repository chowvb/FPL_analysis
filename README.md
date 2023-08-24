Scrape fpl database for generic team and individual statistics (clean_data.py) and save useful stats to .csv for offline viewing 

clean_data.py functions
|Name|Description|Arguments|Return|
|---|---|---|---|
|scrape_and_clean_player_data| Takes data from FPL api, saves a local copy. Cleans the data replacing column names, team id -> names and removes unwanted columns | None | useful_player_stats dataframe & other_stats dataframe|