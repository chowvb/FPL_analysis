import requests, json
import pandas as pd
from pprint import pprint
URL = "https://fantasy.premierleague.com/api/fixtures/"

fixtures_json = requests.get(URL).json()
fixtures_df = pd.DataFrame(fixtures_json)