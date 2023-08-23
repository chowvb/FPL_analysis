"""
main.py 
"""
import clean_data as cd
import player_analysis as pa
import team_analysis as pa

# Define the endpoint that links the fantasy.premierleague API
url = "https://fantasy.premierleague.com/api/"

# Loads data using the url defined above, If there is a network error, the variables are loaded from the player database stored locally. 
useful_data, other_data = cd.scrape_and_clean_player_data(url + "bootstrap-static/")

