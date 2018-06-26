import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
###connect to the database to read sql queries
path ='c:/users/guest/downloads/'
conn= sqlite3.connect(path+'database.sqlite')

###define check_years function to count the number of matches per year to know if there are years
###with little number of matches compared to others to exclude them from analysis
def check_years():
    df_check_years = pd.read_sql_query("""SELECT match_year,COUNT(*) AS num
    FROM (SELECT substr(date,1,4) AS match_year
    FROM  match) AS match_year
    GROUP BY 1
    ORDER BY 2
    """,conn)
    return df_check_years

###def the df_years function to return the number of vectories for each team per year
###passing the year argument as a variable
def df_years(year):
    df_year = pd.read_sql_query("""WITH winners AS(SELECT  substr(date,1,4) as match_year ,
    CASE WHEN home_team_goal > away_team_goal THEN home_team_api_id
    WHEN  home_team_goal < away_team_goal THEN away_team_api_id END AS winning_team_api_id
    FROM match
    )

    SELECT winning_team_api_id,t.team_long_name,COUNT(*) AS total
    FROM winners w
    JOIN team t
    ON t.team_api_id = w.winning_team_api_id
   WHERE match_year = (?)
   GROUP BY 1,match_year
   ORDER BY 3 DESC""",conn,params = (year,))

    return df_year

###define the inner_merge function to make an inner merge between two dataframes
###and test it for missing values,drop the repeated column,and renaming two columns
###according to the number of years
def inner_merge(df1,df2,label1,label2):
    df_merge = pd.merge(df1,df2,on = 'winning_team_api_id')
    df_merge.isnull().sum()
    df_merge.drop('team_long_name_y',axis =1,inplace = True)
    df_merge.rename(columns={"total_x":label1,"total_y":label2},inplace = True)
    return df_merge

###define the diffrence function to add a new column in a data frame to calculate
###the diffrence between two columns,then describe the resulting column,query the
### all rows with have the maximum diffrence,plot a histogram fot the diff column
def diffrence(df):
    df['diff'] = df.iloc[:,2] - df.iloc[:,3]
    print("\n the description of the diffrence between two years:\n",
    df['diff'].describe())
    print("\nprint the teams names have the maximum improvment: \n",
    df.query('diff == diff.max()'))
    df['diff'].hist(color= 'g')
    plt.show()

###passing the 2015 and 2009 as arguments in the df_years function and merge them
###then passing the result to the diffrence function to know the rows that have
###the maximum diffrencein number of vectories in 2015 and 2009
if __name__ =='__main__':
    print("\n print the number of vectories for each team per year:\n")
    print(check_years())
    df_2015=df_years('2015')
    df_2009=df_years('2009')
    df_merge= inner_merge(df_2015,df_2009,'total_2015','total_2009')
    print(" \n print the merged and cleaned data frame\n ")
    print(df_merge)
    diffrence(df_merge)
