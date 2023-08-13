"""
main.py 
"""
import player_analysis as pa
import team_analysis as ta 

players_df = pa.update_player_data()
cleaned_players_df = pa.clean_player_data(players_df)


GLK_df = pa.get_basic_stats_GLK(cleaned_players_df).sort_values(by="total_points", ascending = False)
GLK_df = GLK_df.reset_index(drop=True)

DEF_df = pa.get_basic_stats_DEF(cleaned_players_df).sort_values(by="total_points", ascending = False)
DEF_df = DEF_df.reset_index(drop = True)

MID_df = pa.get_basic_stats_MID(cleaned_players_df).sort_values(by="total_points", ascending = False)
MID_df = MID_df.reset_index(drop = True)

FWD_df = pa.get_basic_stats_FWD(cleaned_players_df).sort_values(by="total_points", ascending = False)
FWD_df = FWD_df.reset_index(drop= True)

def player_economy(df):
    def points_per_cost(points, price):
        # Define the equation to be used to calculate player economy
        ppc = points / (price/10)

        return ppc

    def average_points_per_minute(points, minutes):
        # Define the equation to be used to calculate player economy
        appm = points/ minutes

        return appm
    
    economy_list = []

    for player in range(len(df["id"])):
        ppc = points_per_cost(df["total_points"].iloc[player], df["price"].iloc[player])
        print(df["name"].iloc[player], ":",ppc)
        economy_list.append(ppc)
    
    df["points_per_million"] = economy_list
    return df

