import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
###create the connection to the database
path ='c:/users/guest/downloads/'
conn= sqlite3.connect(path+'database.sqlite')
###perform the sql query that count the number of matches per league over all of the time period
df_league = pd.read_sql_query("""SELECT c.id as country_name,c.name as country_name,
                                        l.name as league_name,
                                 count(*) as num_matches
                                 FROM league l
                                 JOIN country c
                                 ON c.id = l.country_id
                                 JOIN match m ON m.league_id = l.id
                                 GROUP BY 1,2,3 """,conn)
### print the dataframe which has the data about the number of matches per league
print(df_league)
print("\n \n showing inforation about the missing values:\n \n ")
print(df_league.info())
###print two lines to sort the output in the prompt
print("\n\n")

locations = np.arange(11)
### put the names of leagues in a list to put it in x-axis ticks
leagues_names = ['Belgium','England','France','Germany','Italy','Netherlands','Poland','Portugal ','Scotland','Spain','Switzerland']
plt.subplots(figsize=(10,10))
plt.bar(df_league['league_name'],df_league['num_matches'],width = .7,alpha = 1,color = 'g')
plt.xticks(locations,leagues_names)
plt.title('the number of matches per league')
plt.xlabel('the league name')
plt.ylabel('number of matches')
plt.show()
