
# coding: utf-8

# In[2]:

import os
import pandas as pd
import sqlite3
import warnings
import math
import numpy as np

warnings.filterwarnings("ignore")

countries = ""
matches = ""
leagues = ""
teams = ""

with sqlite3.connect('/Users/ruhama.ahale/Documents/git_repository/capstone-project/database_with_player_positions.sqlite') as con:
    players = pd.read_sql_query("SELECT * from Player", con)


# In[2]:

# Calculate the preferred play position (X & Y) for each player
from scipy import stats

columns = ['player_api_id', 'player_name', 'matches_played', 'matches_played_in_position', 'preferred_x_position', 'preferred_y_position']
player_positions = pd.DataFrame([[0, 0, 0, 0, 0, 0]], columns=columns)     
cursor = con.cursor()

print("--------------------------------------------------------------------------------------------")
print("Calculations Started")
print("--------------------------------------------------------------------------------------------")

for index, player in players.head().iterrows():
    player_api_id = player['player_api_id']
    player_name = player['player_name']
    matches_played = 0
    print(str(index + 1) + ". Calculating positions for " + player_name)
    print("--------------------------------------------------------------------------------------------")
    x_positions_array = []
    y_positions_array = []
    for player_number in range(1,12):
        # Get X positions from home matches for the player
        x_positions = cursor.execute("""SELECT home_player_X%d FROM Match WHERE home_player_%d = '%d'""" % (player_number, player_number, player_api_id)).fetchall()
        if len(x_positions) > 0:
            matches_played += len(x_positions)
            x_positions = [x_position[0] for x_position in x_positions]
            x_positions_array += x_positions
            
        # Get X positions from away matches for the player
        x_positions = cursor.execute("""SELECT away_player_X%d FROM Match WHERE away_player_%d = '%d'""" % (player_number, player_number, player_api_id)).fetchall()
        if len(x_positions) > 0:
            matches_played += len(x_positions)
            x_positions = [x_position[0] for x_position in x_positions]
            x_positions_array += x_positions
        
        # Get Y positions from home matches for the player
        y_positions = cursor.execute("""SELECT home_player_Y%d FROM Match WHERE home_player_%d = '%d'""" % (player_number, player_number, player_api_id)).fetchall()
        if len(y_positions) > 0:
            y_positions = [y_position[0] for y_position in y_positions]
            y_positions_array += y_positions
            
        # Get X positions from away matches for the player
        y_positions = cursor.execute("""SELECT away_player_Y%d FROM Match WHERE away_player_%d = '%d'""" % (player_number, player_number, player_api_id)).fetchall()
        if len(y_positions) > 0:
            y_positions = [y_position[0] for y_position in y_positions]
            y_positions_array += y_positions

    # Filter None values from the positions
    x_positions_array = list(filter(None, x_positions_array))
    y_positions_array = list(filter(None, y_positions_array))
    
    # Use mode to get the positions where the player plays most frequently
    preferred_x_position = stats.mode(x_positions_array)[0][0]
    preferred_y_position = stats.mode(y_positions_array)[0][0]
    matches_played_in_position = max(stats.mode(x_positions_array)[1][0], stats.mode(y_positions_array)[1][0])
    
    # Move the data to a dataframe
    player_data = [player_api_id, player_name, matches_played, matches_played_in_position, preferred_x_position, preferred_y_position]
    player_data_frame = pd.DataFrame([player_data], columns=columns)
    player_positions = player_positions.append(player_data_frame, ignore_index=True)

print("Calculations Completed")
print("--------------------------------------------------------------------------------------------")
player_positions = player_positions.drop(player_positions.index[0])
player_positions.head()


# In[3]:

# Define a player position based on the X and Y position combinations
def playerPositionForPrefferedPositions(preferred_x_position, preferred_y_position):
    if (preferred_x_position == 1 and preferred_y_position == 1):
        return 'Goalkeeper'
    if (preferred_x_position in (1, 2) and preferred_y_position == 3):
        return 'Right Back'
    if (preferred_x_position in (3, 4, 5, 6, 7) and preferred_y_position == 3):
        return 'Center Back'
    if (preferred_x_position in (8, 9) and preferred_y_position == 3):
        return 'Left Back'
    if (preferred_x_position in (1, 2, 3) and preferred_y_position in (5, 6)):
        return 'RIght Midfielder'
    if (preferred_x_position == 3 and preferred_y_position == 7):
        return 'RIght Midfielder'
    if (preferred_x_position in (4, 5, 6) and preferred_y_position in (5, 6, 7)):
        return 'Central Midfielder'
    if (preferred_x_position == 7 and preferred_y_position == 7):
        return 'Left Midfielder'
    if (preferred_x_position in (7, 8, 9) and preferred_y_position in (5, 6)):
        return 'Left Midfielder'
    if (preferred_x_position in (1, 2) and preferred_y_position in (7, 8, 9)):
        return 'Right Winger'
    if (preferred_x_position in (3, 4, 5, 6, 7) and preferred_y_position in (8, 9)):
        return 'Attacking Midfielder'
    if (preferred_x_position in (8, 9) and preferred_y_position in (7, 8, 9)):
        return 'Left Winger'
    if (preferred_x_position in (1, 2, 3) and preferred_y_position in (10, 11)):
        return 'Right Forward'
    if (preferred_x_position in (4, 5, 6) and preferred_y_position in (10, 11)):
        return 'Center Forward'
    if (preferred_x_position in (7, 8, 9) and preferred_y_position in (10, 11)):
        return 'Left Forward'
    return 'Position Unknown'

# Calculate the player position for all players
for index, player in player_positions.iterrows():
    preferred_x_position = player['preferred_x_position']
    preferred_y_position = player['preferred_y_position']
    player_position = playerPositionForPrefferedPositions(preferred_x_position, preferred_y_position)
    player_positions.set_value(index, 'player_position', player_position)
    
player_positions.head()


# In[4]:

# Store the dataframe to sqlite
import sqlite3
connection = sqlite3.connect("database.sqlite")
player_positions.to_sql('Player_Positions', connection, if_exists = 'replace', index = False)


# In[ ]:



