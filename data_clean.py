import pandas as pd
import csv

# Define two teams that will be used as an example to compare statistics for different parameters 
team1 = "Liverpool"
team2 = "Everton"
# Creativity.csv contains the Squad goal and Shot Creation table from fbref 
"""
SCA
SCA - Shot creating actions
SCA90 - Shot creating actions per 90 minutes 

SCA Types
PassLive - Live ball passes that lead to a shot attempt 
PassDead - Dead ball passes that lead to a shot attempt 
    eg., Free kick, Corner kicks, Throw-ins, Kickoffs and Goal Kicks 
TO - Successful take ons that leads to a shot attempt 
Sh - Shots that lead to another shot attempt 
Fld - Fouls drawn that leads to another attempt 
Def - Defensive actions that lead to another shot 

GCA 
GCA - Goal Creating Actions 
GCA90 - Goal creating actions per 90 minutes 

GCA types 
PassLive - Completed live ball passes that lead to a goal 
PassDead - Completed dead ball passes that lead to a goal 
TO - Successful take ons that lead to a goal
Sh - Shots that lead to a goal 
Fld - Fouls drawn that leads to a goal 
Def - Defensive actions that lead to a goal
"""
creativity = pd.read_csv("team_data/creativity.csv", header= [0,1], index_col= 0)

# Filter creativity df for only Shot Creating Actions
creativity_SCA = creativity[["Unnamed: 0_level_0", "SCA", "SCA Types"]].droplevel(0, axis= 1)

# Filter creativity df for only Goal Creating Actions
creativity_GCA = creativity[["Unnamed: 0_level_0", "GCA", "GCA Types"]].droplevel(0, axis= 1)


# Defence.csv contains tackles, challenges and blocks for premier league teams
"""
Tackles 
Tkl - Number of Tackles 
TklW - Number of Tackles won
Def 3rd - Number of Tackles in the defensive third 
Mid 3rd - Number of Tackles in the midfield third
Att 3rd - Number of Tackles in the attacking third 

Challenges 
Tkl - Number of dribblers Tackled 
Att - Number of unsuccessful challenges plus number of dribblers tackled
Tkl% - Percentage of dribblers tackled
Lost - Number of unsucessful attempts to challenge a dribbling player

Blocks 
Blocks - Number of times blocking the ball by standing in its path 
Sh - Number of times a shot is blocked 
Pass - Number of passes blocked 
Int - Interceptions
Tkl+Int - Number of players tackled pluss the number of interrceptions
Clr - Clearances 
Err - Mistakes leading to an opponent shot 
"""
defence = pd.read_csv("team_data/defence.csv", header = [0,1], index_col= 0)

# Filter defence df for only Tackles 
defence_tackles = defence[["Unnamed: 0_level_0", "Tackles"]].droplevel(0, axis= 1)

# Filter defence df for only Challenges 
defence_challenges = defence[["Unnamed: 0_level_0", "Challenges"]].droplevel(0, axis = 1)

# Filter defence df for only Blocks
defence_blocks = defence[["Unnamed: 0_level_0", "Blocks"]].droplevel(0, axis = 1)


# Goalkeeping_adv contains indepth stats for goalkeepers in the premier league
"""
Expected
PSxG - Post shot expected goals (How likely that a goalkeeper will save the shot)
PSxG/SoT - Post shot expected goals per Shot on Target (Expected goals based on how likely the goalkeeper is to save the shot)
PSxG+/- - Post shot expected goals minus Goals Allowed (Positive numbers suggest better luck or an above average aility to stop shots)
/90 - Post shot expected goals minus Goals Allowed per 90 minutes 

Launched 
Cmp - Passes Completed longer than 40 yards
Att - Long passes attempted (Longer than 40 yards)
Cmp% - Long pass completion percentage

Passes 
Att(GK) - Passes attempted (Not including goalkicks)
Thr - Throws attempted
Launch% - Percentage of passes longer than 40 yards (Not including goal kicks)
AvgLen - Average length of passes in yards

Goal Kicks 
Att - Goal kick attempts 
Launch% - Percentage of Goal Kicks that were launched 
AvgLen - Average length of Goal Kicks in yards 

Crosses 
Opp - Opponents attempted crosses into penalty areas
Stp - Number of crosses into penalty are that were successfully stopped by the keeper
Stp% - Percentage of crosses into penalty area which were successfully stopped by the goalkeeper

Sweeper
#OPA - Number of defensive actions outside of penalty area
#OPA/90 - Number of defensive actions outside the penalty area per 90 minutes 
AvgDist - Average distance from goal (in yards) of all defensive actions
"""
goalkeeping = pd.read_csv("team_data/goalkeeping_adv.csv", header = [0,1], index_col= 0)

# Filter goalkeeping df for Goals
goalkeeping_goals = goalkeeping[["Unnamed: 0_level_0", "Goals"]].droplevel(0, axis = 1)

# Filter goalkeeping df for expected stats 
goalkeeping_x = goalkeeping[["Unnamed: 0_level_0", "Expected"]].droplevel(0, axis = 1)

# Filter goalkeeping df for launched (Passing)
goalkeeping_launched = goalkeeping[["Unnamed: 0_level_0", "Launched"]].droplevel(0, axis= 1)

# Filter goalkeeping df for goalkeeper passing stats 
goalkeeping_passing = goalkeeping[["Unnamed: 0_level_0", "Passes"]].droplevel(0, axis = 1)

# Filter goalkeeping df for goal kick statistics
goalkeeping_goal_kicks = goalkeeping[["Unnamed: 0_level_0", "Goal Kicks"]].droplevel(0, axis = 1)

# Filter goalkeeping df for crosses 
goalkeeping_crosses = goalkeeping[["Unnamed: 0_level_0", "Crosses"]].droplevel(0, axis = 1)

# Filter goalkeeping df for sweeper keeper statistics 
goalkeeping_sweeper = goalkeeping[["Unnamed: 0_level_0", "Sweeper"]].droplevel(0, axis = 1)


# possession.csv contains team possession stats
"""
Touches 
Touches - Number of times a player has touched the ball 
Def Pen - Touches in defensive penalty area
Def 3rd - Touches in defensive third
Mid 3rd - Touches in midfield third
Att 3rd - Touches in attacking third
Att Pen - Touches in the attacking penalty area
Live - Live ball touches (Does not include corner kicks, freekicks, throw-ins, kick-offs, goalkicks or penaltys)

Take-Ons
Att - Number of attemps to take on defenders while dribbling
Succ - Number of defenders taken on successfully (Dribbling past them)
Succ% - Percentage of take-ons completed successfully 
Tkld - Number of times tackled by defenders during a take-on 
Tkld% - Percentage of time tackled by a defender during a take-on attempt

Carries 
Carries - Number of times a player controlled the ball with their feet
TotDist - Total distance players have carried the balls with their feet (Yards)
PrgDist - Progressive distance, total distance players have carried the ball towards the opposition goal
PrgC - Carries that move the ball towards the goal line
1/3 - Carries into the final third
CPA - Carries into the penalty area
Mis - Miscontrols (Number of times a players have failed to gain control of the ball)
Dis - Dispossessed (number of times a player loses controll of the ball after being tackled)

Receiving 
Rec - Number of times player receives the ball successfully
PrgR - Number of passes that move the ball towards the oppoenents goal.
"""

possession = pd.read_csv("team_data/possession.csv", header = [0,1], index_col= 0)

# Filter possession df for only touches
possession_touches = possession[["Unnamed: 0_level_0", "Touches"]].droplevel(0, axis = 1)

# Filter possession df for only take-ons
possession_takeons = possession[["Unnamed: 0_level_0", "Take-Ons"]].droplevel(0, axis = 1)

# Filter possession df for ball carries 
possession_carries = possession[["Unnamed: 0_level_0", "Carries"]].droplevel(0, axis = 1)

# Filter possession df for receiving stats
possession_receiving = possession[["Unnamed: 0_level_0", "Receiving"]].droplevel(0, axis = 1)


# shooting.csv contains the stats for premier league shooting numbers
"""
Standard
Gls - Goals Scored
Sh - Total Shots
SoT - Shots on Target
Sot% - Percentage shots on target
Sh/90 -  Shots per 90 minutes
SoT/90 - Shots on Target per 90
G/Sh - Goals per shots
G/Sot - Goals per shots on target 
Dist - Average shot distance (Yards)
FK - Shots from Freekicks
PK - Penalty kicks made
PKatt - Penalty kicks attempted

Expected 
xG - Expected goals
npxG - Non-penalty expected goals
npxG/Sh - Non-Penalty Expected goals per shot
G-xG - Goals - Expected goals (Goals scored against expected goals scored)
np:G-xG - Non-penalty Goals - Non-Penalty expected goals (Non-penalty goals against expected non-penalty goals)
"""
shooting = pd.read_csv("team_data/shooting.csv", header = [0,1], index_col= 0)

# Filter shooting stats for standard stats only 
shooting_standard = shooting[["Unnamed: 0_level_0", "Standard"]].droplevel(0, axis = 1)

# Filter shooting stats for expected statistics only
shooting_expected = shooting[["Unnamed: 0_level_0", "Expected"]].droplevel(0, axis = 1)

shooting_g_xg = pd.merge(shooting_expected[["Squad", "xG"]], shooting_standard[["Squad", "Gls"]])


# passing.csv contains passing statistics for premier league clubs
"""
Total 
Cmp - Completed passes 
Att - Passes attempted
Cmp% - Pass completion rate (%)
TotDist - Total passing distance (Yards)
PrgDist - Total passing distance towards opponent goal (Yards)

Short
Cmp - Completed Passing
Att - Attempted passes 
Cmp% - Percentage passes completed

Medium
Cmp - Completed Passing
Att - Attempted passes 
Cmp% - Percentage passes completed

Long
Cmp - Completed Passing
Att - Attempted passes 
Cmp% - Percentage passes completed

other 
Ast - Assists
xAG - Expected assisted goals
xA - Expected assists
A-AxG - Assists minus expected assists
KP - Key Passes 
1/3 - Passes into final third
PPA - Passes into the penalty area
CrsPA - Crosses into the penalty area
ProgP - Total progressive passes (Total Passes forward towards the opponent goal)
"""

passing = pd.read_csv("team_data/passing.csv", header = [0,1], index_col= 0)

passing_overall = passing[["Unnamed: 0_level_0", "Total"]].droplevel(0, axis = 1)
passing_short = passing[["Unnamed: 0_level_0", "Short"]].droplevel(0, axis = 1)
passing_medium = passing[["Unnamed: 0_level_0", "Medium"]].droplevel(0, axis = 1)
passing_long = passing[["Unnamed: 0_level_0", "Long"]].droplevel(0, axis = 1)
passing_other = passing[["Unnamed: 0_level_0", "Unnamed: 17_level_0", "Unnamed: 18_level_0",
                          "Expected", "Unnamed: 21_level_0", "Unnamed: 22_level_0", "Unnamed: 23_level_0",
                          "Unnamed: 24_level_0", "Unnamed: 25_level_0"]].droplevel(0, axis = 1)