import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utility import team_replace_dict_fbref, team_replace_dict2

"""
Scrapes all of the Premier League Teams unique id (to scrape further data from fbref), extension and the team names (fbref version).
The fpl team id and fpl team name is merged to the dataframe. 
Dataframe is saved into a .csv file on the local drive.
"""
def unique_team_id():
    # Request Premier League Stats from fbref
    r = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")

    # Read the requested html and parser it. 
    soup = BeautifulSoup(r.text, "html.parser")

    # Select the stats table within the html parser
    standings_table = soup.select("table.stats_table")[0]

    #
    teams = standings_table.find_all("a")
    
    # For each of the teams there is a href corresponding to them
    links = [l.get("href") for l in teams]
    team_urls = [f"https://fbref.com{l}" for l in links] # Get the url for each of the Premier League teams individual fbref web pages 
    teams_list = []
    for i, team in enumerate(teams):
        teams_list.append(teams[i].text)
    
    # Create a dataframe to store the Team names and the corresponding links. 
    team_df = pd.DataFrame({
        "Team": teams_list,
        "Link": team_urls
        })
    
    # 
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

"""
Scrapes all the unique id numbers for all Premier League players on the fbref database.
Returns a table with the player name and their unique extension.
"""
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

"""
Scrapes tables of team data from fbref website for different tables and saves them in individual .csv files. For offline analysis.
"""
def update_team_statistics():
    # Create a dictionary for the names, of the different tables found on fbref and the corresponding table_id tags within the html file.
    pl_stats = {
    "stats_type": ["possession","pl_table","general_stats","goalkeeping", "goalkeeping_adv", "shooting", "passing", "creativity", "defence", "possession", "other"],
    "html_table_id": ["stats_squads_possession_for","results2023-202491_overall", "stats_squads_standard_for" ,"stats_squads_keeper_for", "stats_squads_keeper_adv_for", "stats_squads_shooting_for", "stats_squads_passing_for",
                      "stats_squads_gca_for", "stats_squads_defense_for", "stats_squads_posession_for", "stats_squads_misc_for"]
                      }
    
    # Turn the dictionary into a dataframe
    pl_stats_df = pd.DataFrame(pl_stats)

    # enumerate through each html tag
    for i, id in enumerate(pl_stats["html_table_id"]):
        
        # Send a HTML request to fbref's website
        r = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")

        # Use BeautifulSoup to parse the data from the web request
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Using the id in the eunmerate (each of the html table id's.)
        table = soup.find("table", {"id": id})
        
        # if there is a table present continue to save the table as a .csv file using pandas to read the html text. 
        if table:
            df = pd.read_html(str(table))[0]
            file_name = pl_stats_df["stats_type"][i] # using the index for the enumerate loop find the name of the fbref table 
            df.to_csv(f"fbref_data/team_data/{file_name}.csv") # Save the table as a .csv file.


def get_stats():
    """
    Scrape fbref websites and obtain data for player statistics based on different tables. ***FUNCTION NOT OPERATIONAL SEE NOTE BELOW***
    
    Note: FBref's anti bot system will cause the function to break and return empyty csv files as the system will only allow for a certain number of webscrapes within a timeframe.
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
        
    