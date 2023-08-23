import csv, requests, json
import pandas as pd
import numpy as np 
import os

def scrape_and_clean_player_data(api_link):
    # Define columns to delete and seperated into a seperate DataFrame
    other_columns = {
        "old_names": ["id", "first_name","second_name", "web_name", "team", "element_type", "chance_of_playing_next_round", "chance_of_playing_this_round","team_code","transfers_in", "transfers_in_event",
                "transfers_out", "transfers_out_event", "now_cost_rank", "now_cost_rank_type", "form_rank", "form_rank_type","points_per_game_rank",
                "points_per_game_rank_type","code", "cost_change_event", "cost_change_event_fall", "dreamteam_count", "in_dreamteam", "news", "news_added",
                "photo", "special", "squad_number", "status", "corners_and_indirect_freekicks_text", "direct_freekicks_text", "penalties_text", "selected_rank",
                "selected_rank_type", "influence_rank", "influence_rank_type", "creativity_rank", "creativity_rank_type", "threat_rank", "threat_rank_type",
                "ict_index_rank", "ict_index_rank_type"],
        
        "new_names" : ["id", "first_name","second_name", "web_name", "team", "position", "chance_of_playing_next_round", "chance_of_playing_this_round","team_code","transfers_in", "transfers_in_event",
                "transfers_out", "transfers_out_event", "now_cost_rank", "now_cost_rank_type", "form_rank", "form_rank_type","points_per_game_rank",
                "points_per_game_rank_type","code", "cost_change_event", "cost_change_event_fall", "dreamteam_count", "in_dreamteam", "news", "news_added",
                "photo", "special", "squad_number", "status", "corners_and_indirect_freekicks_text", "direct_freekicks_text", "penalties_text", "selected_rank",
                "selected_rank_type", "influence_rank", "influence_rank_type", "creativity_rank", "creativity_rank_type", "threat_rank", "threat_rank_type",
                "ict_index_rank", "ict_index_rank_type"]

    }

    # Define columns to be kept in the main dataframe, and any amendments to column names to easier to understand titles.
    df_columns = {
        "old_names": ["id", "first_name","second_name", "web_name", "team", "element_type", "selected_by_percent", "now_cost","cost_change_start", "cost_change_start_fall",
                    "value_form", "value_season", "total_points", "event_points", "bps", "points_per_game", "ep_next", "ep_this", "form", "starts", "minutes",
                    "goals_scored", "expected_goals", "assists", "expected_assists", "expected_goal_involvements", "clean_sheets", "goals_conceded", "expected_goals_conceded",
                    "own_goals", "penalties_saved", "penalties_missed", "yellow_cards", "red_cards", "saves", "bonus", "influence", "creativity", "threat", "ict_index",
                    "expected_goals_per_90", "expected_assists_per_90", "clean_sheets_per_90", "expected_goal_involvements_per_90", "expected_goals_conceded_per_90", 
                    "goals_conceded_per_90", "saves_per_90", "starts_per_90", "corners_and_indirect_freekicks_order", "direct_freekicks_order", "penalties_order"],

        "new_names": ["id", "first_name","second_name", "web_name", "team", "position", "selected_by_percent", "price","cost_change_start", "cost_change_start_fall",
                    "value_form", "value_season", "total_points", "gw_points", "bps", "points_per_game", "expected_points_next", "expected_points_this", "form", "starts", "minutes",
                    "goals", "xg", "assists", "xa", "xgi", "clean_sheets", "goals_conceded", "xgc",
                    "own_goals", "penalties_saved", "penalties_missed", "yellow_cards", "red_cards", "saves", "bonus", "influence", "creativity", "threat", "ict_index",
                    "xg_per_90", "xa_per_90", "clean_sheets_per_90", "xgi_per_90", "xgc_per_90", 
                    "goals_conceded_per_90", "saves_per_90", "starts_per_90", "set_piece_order", "direct_freekicks_order", "penalties_order"]
    }

    # Create a dictionary of the teams and the correspoinding team codes for each of the players 
    team_replace_dict = { 
        1 : "Arsenal",
        2 : "Aston Villa",
        3 : "Bournemouth",
        4 : "Brentford",
        5 : "Bighton",
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

    # Create a dictionary of the position of the players in the raw format and the corrosponding position that that the players play in. 
    position_replace_dict = { 1: "GLK", 2: "DEF", 3 : "MID", 4: "FWD"}   
    
    # Define a function that rearranges the columns within the c_df DataFrame
    def test_function(current_column_name, new_column_name, column_position, dataframe):
        reorder_col = dataframe.pop(current_column_name)
        dataframe.insert(column_position, new_column_name, reorder_col)
    
    # Define a function to rename and rearrange column names for the two dataframes. 
    def sort_columns(dataframe, col_dict, team_replace_dict, position_replace_dict):

        # Loop through the length of the columns and call the test_function()
        for i in range(len(col_dict["new_names"])):
            test_function(
                col_dict["old_names"][i],
                col_dict["new_names"][i],
                i,
                dataframe
            )
            
        # Replace the position from numbers to letters 
        dataframe["position"].replace(position_replace_dict, inplace = True)

        # Replace the teams from numbers to the full name of the club the players play for. 
        dataframe["team"].replace(team_replace_dict, inplace = True)
        return dataframe

    try:
        # Connect with the API and save the data as a .json()
        response = requests.get(api_link)
        response.raise_for_status()
        data = response.json()
        # Filter through the .json() for "elements" == "players"
        players = data["elements"]

        # Convert the .json() into a pandas DataFrame for easier analysis. 
        players_df = pd.DataFrame(players)

        # Save the DataFrame to .csv file for offline analysis 
        players_df.to_csv("data/2023-2024/players_raw.csv", index = False)

        

        # Create a new DataFrame that contains the wanted columns and unwanted columns
        cleaned_df = players_df[df_columns["old_names"]]
        
        # Create a new DataFrame that contains the wanted calumns and unwanted columns
        other_df = players_df[other_columns["old_names"]]

        # Call upon the sort columns for both of the dataframes to rename columns and clean the dataframes. 
        useful_player_stats_df = sort_columns(cleaned_df, df_columns ,team_replace_dict, position_replace_dict)
        other_stats_df = sort_columns(other_df, other_columns, team_replace_dict, position_replace_dict)

        # Create a DataFrame with only the id, Name, team and position and save to a .csv file for offline analysis
        player_id_df = cleaned_df[["first_name", "second_name", "id"]]
        player_id_df.to_csv("data/2023-2024/player_idlist.csv", index=False)

        # Create a DataFrame to the same format as 2022-2023/cleaned_players.csv format for easy analysis and comparison to previous season.
        cleaned_players_df = players_df[["first_name", "second_name", "goals_scored", "assists", "total_points",
                                        "minutes", "goals_conceded", "creativity", "influence", "threat", "bonus",
                                        "bps", "ict_index", "clean_sheets", "red_cards", "yellow_cards", "selected_by_percent",
                                        "now_cost", "element_type"]]
        
        # Replace element_type numbers with corresponding positions
        cleaned_players_df["element_type"].replace(position_replace_dict, inplace = True)
        
        # Save the cleaned_players_df to a .csv file for offline analysis
        cleaned_players_df.to_csv("data/2023-2024/cleaned_players.csv", index = False)

        return useful_player_stats_df, other_stats_df
    

    except requests.exceptions.RequestException as e:
        print("An error occured:", e )

        file_path = "data/2023-2024/players_raw.csv"
        def check_offline_file(file_path):
            return os.path.exists(file_path)
        
        if check_offline_file(file_path):
            print("Loading locally saved database")
            players_df = pd.read_csv("data/2023-2024/players_raw.csv")

            # Create a new DataFrame that contains the wanted columns and unwanted columns
            cleaned_df = players_df[df_columns["old_names"]]
            
            # Create a new DataFrame that contains the wanted calumns and unwanted columns
            other_df = players_df[other_columns["old_names"]]

            # Call upon the sort columns for both of the dataframes to rename columns and clean the dataframes. 
            useful_player_stats_df = sort_columns(cleaned_df, df_columns ,team_replace_dict, position_replace_dict)
            other_stats_df = sort_columns(other_df, other_columns, team_replace_dict, position_replace_dict)

            return useful_player_stats_df, other_stats_df
        
        else:
            print("No offline player Database available to load")
