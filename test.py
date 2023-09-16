import requests
from bs4 import BeautifulSoup
import pandas as pd 


url = "https://fbref.com/en/players/e46012d4/Kevin-De-Bruyne"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

player_table_id  = "scout_summary_MF"

table = soup.find("table", {"id":player_table_id})

df = pd.read_html(str(table))
