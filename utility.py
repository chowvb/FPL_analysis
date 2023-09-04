import requests
import pandas as pd
from bs4 import BeautifulSoup
team_replace_dict = { 
        1 : "Arsenal",
        2 : "Aston Villa",
        3 : "Bournemouth",
        4 : "Brentford",
        5 : "Brighton",
        6 : "Burnley",
        7 : "Chelsea",
        8 : "Crystal Palace", 
        9 : "Everton",
        10 : "Fulham",
        11 : "Liverpool",
        12 : "Luton",
        13 : "Man City",
        14 : "Man Utd",
        15 : "Newcastle",
        16 : "Nott'm Forrest",
        17 : "Sheffield Utd",
        18 : "Spurs",
        19 : "West Ham",
        20 : "Wolves"
    }
team_replace_dict2 = {"team_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                         "Team": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford",
                                "Brighton", "Burnley", "Chelsea", "Crystal Palace", 
                                "Everton", "Fulham", "Liverpool", "Luton", "Man City",
                                "Man Utd", "Newcastle", "Nott'm Forrest", "Sheffield Utd",
                                "Spurs", "West Ham","Wolves"]
    }


team_replace_dict_fbref = {"fpl_team_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                         "Team": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford",
                                "Brighton", "Burnley", "Chelsea", "Crystal Palace", 
                                "Everton", "Fulham", "Liverpool", "Luton Town", "Manchester City",
                                "Manchester Utd", "Newcastle Utd", "Nott'm Forrest", "Sheffield Utd",
                                "Tottenham", "West Ham","Wolves"]
    }