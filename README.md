Scrape fpl database for generic team and individual statistics (clean_data.py) and save useful stats to .csv for offline viewing 

==FPL Team_ID==
|ID|Team|
|---|---|
|1|Arsenal|
|2|Aston Villa|
|3|Bournemouth|
|4|Brentford|
|5|Brighton|
|6|Burnley|
|7|Chelsea|
|8|Crystal Palace|
|9|Everton|
|10|Fulham|
|11|Liverpool|
|12|Luton Town|
|13|Manchester City|
|14|Manchester United|
|15|Newcastle United|
|16|Nottingham Forest|
|17|Sheffield United|
|18|Tottenham Hotspur|
|19|West Ham United|
|20|Wolverhampton Wanderers|
==clean_data.py ==
|Name|Description|Arguments|Return|
|---|---|---|---|
|scrape_and_clean_player_data() | Takes data from FPL api, saves a local copy. Cleans the data replacing column names, team id -> names and removes unwanted columns | None | Two DataFrames: useful_player_stats dataframe, other_stats dataframe|

