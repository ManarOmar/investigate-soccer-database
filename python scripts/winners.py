import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

###create the connection to the database
path ='c:/users/guest/downloads/'
conn= sqlite3.connect(path+'database.sqlite')
###perform the sql query that catch the id of each match with a new column has the winner
### team type(H,A,D)for (home,away,draw)
df_winner = pd.read_sql_query("""SELECT id,CASE WHEN home_team_goal > away_team_goal THEN 'HOME'
            WHEN home_team_goal < away_team_goal THEN 'AWAY' WHEN home_team_goal = away_team_goal
             THEN  'DRAW' END AS winner FROM match""",conn)

###test if there are null values in the data frame df_winner
print("\n \n showing if there are null values")

print(df_winner.isnull().any())
print("\n \n")

###create a new data frame showing the number of vectories for each team type
df_winner_count = df_winner.groupby('winner').count()
print(df_winner_count)

###plot the data frame using matplotlib
plt.bar(df_winner_count.index,df_winner_count['id'])
plt.title('number of vectories and draw for home and away teams')
plt.ylabel('number of vectories')
plt.xlabel('types of the teams')
plt.show()
