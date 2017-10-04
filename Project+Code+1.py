
# coding: utf-8

# **Predicting the best players by strength of players for playing positions**

# **The Problem:** The client, a famous European Football Club wants to have a list of players to consider during transfer season. In case they need to make a transfer, they will bring in a replacement. A major part of player selection depends upon which position the player will play at. Depending on the need of the team, the managers will consider the up and coming players who will suit their need. The client requires us to build an algorithm that will predict the best 20 players for each specific position

# **The Solution:** 
# 
# **Data:** The data we will use for this problem is sourced from several websites such as 
# 
# http://football-data.mx-api.enetscores.com/ : scores, lineup, team formation and events
# 
# http://www.football-data.co.uk/ : betting odds
# 
# http://sofifa.com/ : players and teams attributes from EA Sports FIFA games. FIFA series and all FIFA assets property of EA Sports;
# by Hugomathien and made available on Kaggle at https://www.kaggle.com/hugomathien/soccer
# 
# **Cleaning:** 
# 1. From the available database, we use the tables 'players' and 'player_attributes' and identify each players preferred position of playing using their X, Y playing coordinates. We create a table of player_positions to make merging of datasets easier
# 2. After merging all the available datasets, we keep only the features we need to predict the performance for a player. We use the feature 'overall_rating' given by FIFA and we calculate the age of each player for the same rating date. This is to understand whether age of the player has impact on player performance. Alternatively, we can also collect rating for each player on the latest date available for the player and use that to correlate age and overall_rating
# 3. We check this data for missing and incorrect values and clean it
# 
# **Descriptive Analytics:**
# 1. Test the correlation of age with overall rating and fit a model to predict rating for each player position
# 2. Also test additional data from player attributes dataset like player strength, height, weight etc. to check for correlation with score (overall_rating)
# 
# **Modeling:**
# 1. For each position, check assumptions, hypotheses and test
# 2. Fit a suitable model on training data and test on testing data
# 

# Step 1: Importing the data and packages required

# In[119]:

#import packages
import os
import pandas as pd
import sqlite3
import warnings
warnings.filterwarnings("ignore")
import datetime as dt
import scipy.stats as stats
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import sklearn

import seaborn as sns

# special matplotlib argument for improved plots
from matplotlib import rcParams
sns.set_style("whitegrid")
sns.set_context("poster")


# In[120]:

#formatting for table displays
from IPython.core.display import HTML
css = open('style-table.css').read() + open('style-notebook.css').read()
HTML('<style>{}</style>'.format(css))


# In[141]:

#connection to database
with sqlite3.connect('/Users/ruhama.ahale/Documents/git_repository/capstone-project/database_with_player_positions.sqlite') as con:
    #countries = pd.read_sql_query("SELECT * from Country", con)
    #matches = pd.read_sql_query("SELECT * from Match", con)
    #leagues = pd.read_sql_query("SELECT * from League", con)
    #teams = pd.read_sql_query("SELECT * from Team", con)
    player_attributes = pd.read_sql_query("SELECT * from Player_Attributes", con)
    player_positions = pd.read_sql_query("SELECT * from Player_Positions", con)
    player = pd.read_sql_query("SELECT * from Player", con)


# Step 2: Joining selected table to create final data table

# In[142]:

player.head(3)


# In[143]:

player_attributes.head(3)


# In[144]:

player_positions.head(3)


# In[145]:

#merge all player files to get the player details required
player_positions = player_positions[['player_api_id', 'player_name', 'player_position']]
player_attributes_new = player_attributes[['player_api_id','date', 'overall_rating']]
player_attributes_new = player_positions.merge(player_attributes_new,on='player_api_id')
player = player[['player_api_id', 'birthday', 'height', 'weight']]
player_attributes_new = player_attributes_new.merge(player,on='player_api_id')
player_attributes_new['birthday_date'] = pd.to_datetime(player_attributes_new['birthday'])
player_attributes_new['date'] = pd.to_datetime(player_attributes_new['date'])
player_attributes_new['age'] = player_attributes_new['date'] - player_attributes_new['birthday_date']
player_attributes_new['age'] = player_attributes_new['age'].astype(dt.timedelta).map(lambda x: np.nan if pd.isnull(x) else x.days)
player_attributes_new['age'] = round(player_attributes_new['age']/365,0)
player_attributes_new = player_attributes_new[player_attributes_new.date >= '2009-07-31']


# In[146]:

player_attributes_new.head(3)


# In[147]:

#number of unique player in our new database
player_attributes_new.player_api_id.nunique()


# In[148]:

#count unique players in each position
player_attributes_new.groupby(player_attributes_new.player_position).player_api_id.nunique()


# In[149]:

#select data for one position for analysis
left_back = player_attributes_new[(player_attributes_new.player_position== 'Left Back')]
left_back_avg = left_back.groupby(left_back.player_api_id).mean()
left_back_avg.head()


# In[138]:

#plot for mean age
plt.hist(left_back_avg.age)
plt.title("Age")
plt.xlabel("Average players per age")
plt.ylabel("Frequency")
plt.show()


# In[150]:

#plot for mean overall_rating
plt.hist(left_back_avg.overall_rating)
plt.title("Overall Rating")
plt.xlabel("Average players per Rating")
plt.ylabel("Frequency")
plt.show()


# In[139]:

#Scatter plot to check relationship between age and rating
plt.scatter(left_back_avg.age, left_back_avg.overall_rating)
plt.xlabel("Player Overall Rating by Age")
plt.ylabel("Age")
plt.title("Rating")


# In[140]:

sns.regplot(y="overall_rating", x="age", data=left_back_avg, fit_reg = True)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



