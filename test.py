"""
Test File. The aim of this script is to develop a way to marry the players names in FPL and the players names in fbref
There are some differences between the two databases eg, A Brazilian player in FPL may contain all names but FBref will only use their known by name.
"""

import pandas as pd

# Read FPL names
fpl_names = pd.read_csv("data/2023-2024/player_idlist.csv")
fpl_names["full_name"] = fpl_names["first_name"] + " " + fpl_names["second_name"].astype(str)
# Read FBref names.
fbref_names = pd.read_csv("fbref_data/player_data/player_endpoints.csv")

fpl_names_list = fpl_names["full_name"]
fpl_names_list = sorted(fpl_names_list)

fbref_names_list = fbref_names["Player"]
fbref_names_list = sorted(fbref_names_list)

partial_matches = []
non_matches = []
import re
for name in fbref_names_list:
    # Partial match pattern
    pattern = re.compile(f"{name}", re.IGNORECASE)  # Change "ap" to the partial match you're looking for

    # Find partial matches and non-matches in the list of strings
    for string in fpl_names_list:
        if re.search(pattern, string):
            partial_matches.append(string)
        else:
            non_matches.append(string)
