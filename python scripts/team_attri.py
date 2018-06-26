import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
path ='c:/users/guest/downloads/'
conn= sqlite3.connect(path+'database.sqlite')

###define the victor function to plot a scatter for the number of vecroties per year for the
###given team_api_id which is passed as an argument
def vector(team_api_id):
    df_vector = pd.read_sql_query("""SELECT *,count(*) as num_vectories
    FROM (SELECT substr(date,1,4) as match_year,CASE WHEN home_team_goal > away_team_goal
    THEN home_team_api_id WHEN  home_team_goal < away_team_goal THEN away_team_api_id
    END AS winning_team_api_id
    FROM match)
    WHERE winning_team_api_id == (?)
    GROUP BY 1,2
    ORDER BY 2""",conn,params = (team_api_id,))
###convert the type of the match year to integer to plot it in a scatter
    df_vector['match_year'] = df_vector['match_year'].astype(int)
    df_vector.plot.scatter(x='match_year',y ='num_vectories')
    plt.show()
    return df_vector

###define the team_attri function to return a cleaned data frame that has data
###for the attributes of the given team_fifa_api_id
def team_attri(team_api_id):
    df_team_attri = pd.read_sql_query("""SELECT *,substr(date,1,4) as match_year
    FROM team_attributes
    WHERE team_api_id = (?) """,conn,params=(team_api_id,))

    df_team_attri.drop('date',axis = 1,inplace = True)
    df_team_attri['match_year'] = df_team_attri['match_year'].astype('int')
    return df_team_attri

###define the merge function to merge the team's victories number with its
###attributes ,check for the names of columns and drop the unwanted columns,THEN
###check again to be sure
def merge(df1,df2):
    df_merge = pd.merge(df1,df2 , on = 'match_year')
    print("\nthe data frame columns before drop:\n",df_merge.columns)
    df_merge.drop(['team_api_id','winning_team_api_id',
    'id','team_fifa_api_id'],axis =1,inplace = True)
    print("\nthe data frame columns after drop:\n",df_merge.columns)
    return df_merge

###define the check_attri function tocheck the missing values for all the
### team_attributes table
def check_attri(df):

    print("\nprint the number of missing values in each"+
    "column:\n",df.isnull().sum())

    print("\n\nprint the unique values in the team attributes in the "+
    "buildUpPlayDribblingClass column\n\n",df['buildUpPlayDribblingClass'].unique())

    print("\n\n",df.loc[:,['buildUpPlayDribbling','buildUpPlayDribblingClass']])


###define dribble_little to fill the missing values in the buildupplaydribbling
###which has a little in the buildupplaydribblingclass column with the average
###of the other rows that have values in buildUpPlayDribbling for the little class
def dribble_little(df):
    df_dribble = pd.read_sql_query("""SELECT AVG(buildupplaydribbling) as avgdribble
    FROM Team_Attributes
    WHERE buildupplaydribblingclass == 'Little'""",conn)
###assigning the mean value (avgdribble) to each row that have little in
###buildUpPlayDribblingClass and null in buildUpPlayDribbling
    df.loc[(df.buildUpPlayDribblingClass == 'Little') & (df.buildUpPlayDribbling.isnull()),
     'buildUpPlayDribbling'] =df_dribble.loc[0,'avgdribble'].astype(int)
    return df

##define dribble_lots to fill the missing values in the buildupplaydribbling
###which has a lots in the buildupplaydribblingclass column with the average
###of the other rows that have values in buildUpPlayDribbling for lots class
def dribble_lots(df):
    df_dribble = pd.read_sql_query("""SELECT AVG(buildupplaydribbling) as avgdribble
    FROM Team_Attributes
    WHERE buildupplaydribblingclass == 'Lots'""",conn)
###assigning the mean value (avgdribble) to each row that have lots in
###buildUpPlayDribblingClass and null in buildUpPlayDribbling
    df.loc[(df.buildUpPlayDribblingClass == 'Lots') & (df.buildUpPlayDribbling.isnull()),
    'buildUpPlayDribbling'] =df_dribble.loc[0,'avgdribble'].astype(int)
    return df

##define dribble_normal to fill the missing values in the buildupplaydribbling
###which has a normal in the buildupplaydribblingclass column with the average
###of the other rows that have values in buildUpPlayDribbling for the normal class
def dribble_normal(df):
    df_dribble = pd.read_sql_query("""SELECT AVG(buildupplaydribbling) as avgdribble
    FROM Team_Attributes
    WHERE buildupplaydribblingclass == 'Normal'""",conn)
###assigning the mean value (avgdribble) to each row that have normal in
###buildUpPlayDribblingClass and null in buildUpPlayDribbling
    df.loc[(df.buildUpPlayDribblingClass == 'Normal') & (df.buildUpPlayDribbling.isnull()),
    'buildUpPlayDribbling'] =df_dribble.loc[0,'avgdribble'].astype(int)
    return df

###define the plot_line function to plot the relationship between number of
###victories and the other attributies which is stored in a list to iterate the
###plotting over its element in a for loop and  Calling plt.pause(0.05)
###to both draw the new data and it runs the GUI's event loop (allowing for mouse interaction).
def plot_line(df):
    list_attri = ['buildUpPlayDribbling', 'buildUpPlaySpeed', 'buildUpPlayPassing',
    'chanceCreationPassing','chanceCreationCrossing', 'chanceCreationShooting',
    'defencePressure','defenceAggression','defenceTeamWidth']

    ax = plt.gca(title ='the relashionship between the number of vicrories and many attributes')
    n=0
    for n in range(len(list_attri)):
        df.plot(kind = 'line' , x = 'num_vectories',y = list_attri[n],ax = ax,figsize=(10,10) )
        plt.pause(0.05)
    plt.show()


if __name__ =='__main__':
    ###passing the team_api_id 8485 which has the maximum diffrence in the number
    ###of victories over the time period to the functions above
    df_aber_vector = vector(8485)
    print(df_aber_vector)
    df_aber_attri = team_attri(8485)
    print(df_aber_attri)
    df_merge_aber = merge(df_aber_vector,df_aber_attri)
    print(df_merge_aber)
    check_attri(df_merge_aber)
    dribble_little(df_merge_aber)
    print("the data frame after fixing the buildupplaydribbling"+
    "missing values: \n")
    print(df_merge_aber['buildUpPlayDribbling'])
    plot_line(df_merge_aber)
