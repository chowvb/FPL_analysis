import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utility import team_replace_dict_fbref, team_replace_dict2

def unique_team_id():
    r = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")
    soup = BeautifulSoup(r.text, "html.parser")
    standings_table = soup.select("table.stats_table")[0]
    teams = standings_table.find_all("a")
    links = [l.get("href") for l in teams]
    team_urls = [f"https://fbref.com{l}" for l in links]
    teams_list = []
    for i, team in enumerate(teams):
        teams_list.append(teams[i].text)
    team_df = pd.DataFrame({
        "Team": teams_list,
        "Link": team_urls
        })
    team_df = team_df[team_df["Link"].str.contains("/squads/")]
    team_df["Path"] = [urlparse(url).path for url in team_df["Link"]]
    team_df = team_df.join(team_df["Path"].str.split("/", expand = True).add_prefix("Path_"))
    team_df = team_df.rename(columns={"Path_3": "unique_team_id", "Path_4": "extension"})
    team_df = team_df[["Team", "unique_team_id", "extension", "Link"]]
    team_df = team_df.replace("Nott'ham Forest", "Nott'm Forest")
    fpl_team_id = pd.DataFrame(team_replace_dict_fbref)
    fpl_team_name = pd.DataFrame(team_replace_dict2)
    merged_team_df = team_df.merge(fpl_team_id, on= "Team")
    merged_team_df = merged_team_df.merge(fpl_team_name, left_on = "fpl_team_id", right_on= "team_id")
    merged_team_df = merged_team_df.drop(columns=["team_id"]).rename(columns={"Team_x" : "Team","Team_y": "fpl_team"})
    merged_team_df.to_csv("fbref_data/team_data/team_id.csv", index= False)
    #return merged_team_df

def unique_player_id():
    r = requests.get("https://fbref.com/en/comps/9//wages/Premier-League-Wages/")
    soup = BeautifulSoup(r.text)
    table = soup.select("table.stats_table")[1]
    players = table.find_all("a")
    links = [l.get("href") for l in players]
    player_urls = [f"https://fbref.com{l}" for l in links]
    player_list = []
    for i, player in enumerate(players):
        player_list.append(players[i].text)
    players_df = pd.DataFrame({
        "Player" : player_list,
        "Link" : player_urls 
        })
    players_df = players_df[players_df["Link"].str.contains("/players/")]
    players_df["Path"] = [urlparse(url).path for url in players_df["Link"]]
    players_df = players_df.join(players_df["Path"].str.split("/", expand=True).add_prefix("Path_"))
    players_df = players_df.rename(columns={"Path_3": "unique_player_id", "Path_4": "extension"})
    players_df = players_df[["Player", "unique_player_id", "extension", "Link"]]

    return players_df

def get_table():
    r = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")
    soup = BeautifulSoup(r.text, "html.parser")

    table_id = "stats_squads_standard_for"
    table = soup.find("table", {"id": table_id})

    if table:
        df = pd.read_html(str(table))[0]

    print(df.head())

def update_team_statistics():
    pl_stats = {
    "stats_type": ["pl_table","general_stats","goalkeeping", "goalkeeping_adv", "shooting", "passing", "creativity", "defence", "possession", "other"],
    "html_table_id": ["results2023-202491_overall", "stats_squads_standard_for" ,"stats_squads_keeper_for", "stats_squads_keeper_adv_for", "stats_squads_shooting_for", "stats_squads_passing_for",
                      "stats_squads_gca_for", "stats_squads_defense_for", "stats_squads_posession_for", "stats_squads_misc_for"]
                      }
    
    pl_stats_df = pd.DataFrame(pl_stats)
    for i, id in enumerate(pl_stats["html_table_id"]):
        r = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"id": id})
        if table:
            df = pd.read_html(str(table))[0]
            file_name = pl_stats_df["stats_type"][i]
            df.to_csv(f"fbref_data/team_data/{file_name}.csv")

def player_stats(team_name):
    team_id = unique_team_id()
    team_name_df = team_id[team_id["Team"] == team_name].reset_index(drop = True)
    url = team_name_df["Link"][0]

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    table_id = "stats_keeper_adv_9"
    table = soup.find("table", {"id" : table_id})

    if table:
        df = pd.read_html(str(table))[0]
        df = df.drop(df.index[-2:], axis = 0)
        df = df.drop(columns= "Per 90 Minutes")
        df = df.droplevel(0, axis = 1)
        df = df.drop(columns = "Matches")
        
    else:
        print("Error: No Table Found")

    return df 

def get_stats():
    """
    Note: FBref's anti bot system will cause the function to break and return empyty csv files as the system will only allow for 
    """
    team_stats = {
    "stats_type" : ["general_stats", "goalkeeping" , "shooting", "passing", "passing_type", "creativity", "defence", "possession", "playing_time", "other_stats"],
    "html_table_id" : ["stats_standard_9", "stats_keeper_adv_9", "stats_shooting_9", "stats_passing_9", "stats_passing_types_9", "stats_gca_9", "stats_defense_9", "stats_possession_9", "stats_playing_time_9", "stats_misc_9"]
    }
    #teams_list = unique_team_id()
    teams_list = pd.read_csv("fbref_data/team_data/team_id.csv")
    
    for i, table_link in enumerate(team_stats["html_table_id"]):
        player_stats = pd.DataFrame()
        print(table_link)
        for team_link in teams_list["Link"]:
            print(team_link + "\n")

            r = requests.get(team_link)
            soup = BeautifulSoup(r.text, "html.parser")

            table = soup.find("table", id = table_link)
            try:
                stats_df = pd.read_html(str(table))[0]

                player_stats = pd.concat([player_stats, stats_df], axis = 0).reset_index(drop = True)

                file_name = team_stats["stats_type"][i]
                #player_stats.to_csv(f"fbref_data/player_data/{file_name}.csv")
            except:
                print(f"Table Error for {team_link}")
        
    