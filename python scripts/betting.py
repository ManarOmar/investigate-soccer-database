import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
path ='c:/users/guest/downloads/'
conn= sqlite3.connect(path+'database.sqlite')

###print the number of rows where Willian hill betting have values and ignore the
###rows that have a missing vlaues in Wiliam hill betting columns(BWH,BWA,BWD)
def num_rows():
    df_bw=pd.read_sql_query("""SELECT bwh,bwd,bwa
    FROM match
    WHERE bwh IS NOT NULL AND bwa IS NOT NULL AND bwd IS NOT NULL""",conn)
    print("showing the shape of the df_bw data frame: \n ")
    print(df_bw.shape)
    print("\n \n ")

###define the avg_odds to compute the average of betting for each result of each
### match ,and using COALESCE function to fill any null value with the famous
### willian hill betting
def avg_odds():
    df_oddsH = pd.read_sql_query("""SELECT  ID,(COALESCE(B365H,BWH) + BWH + COALESCE(IWH,BWH)
    + COALESCE(LBH,BWH) + COALESCE(PSH,BWH) + COALESCE(WHH,BWH) + COALESCE(SJH,BWH) + COALESCE(VCH,BWH)
    + COALESCE(GBH,BWH) + COALESCE(BSH,BWH))/ 10 AS AVGH FROM match """,conn)

    df_oddsA = pd.read_sql_query("""SELECT  ID,(COALESCE(B365A,BWA) + BWA + COALESCE(IWA,BWA) +
    COALESCE(LBA,BWA) + COALESCE(PSA,BWA) + COALESCE(WHA,BWA) + COALESCE(SJA,BWA) +
    COALESCE(VCA,BWA) + COALESCE(GBA,BWA) + COALESCE(BSA,BWA))/ 10 AS AVGA FROM match """,conn)

    df_oddsD = pd.read_sql_query("""SELECT  ID,(COALESCE(B365D,BWD) + BWD + COALESCE(IWD,BWD) +
    COALESCE(LBD,BWD) + COALESCE(PSD,BWD) + COALESCE(WHD,BWD) + COALESCE(SJD,BWD) +
    COALESCE(VCD,BWD) + COALESCE(GBD,BWD) + COALESCE(BSD,BWD))/ 10 AS AVGD FROM match """,conn)

    return (df_oddsH,df_oddsA,df_oddsD)
###define the check_nulls function to check if there are missing values
###and drop the related rows and check again to be sure
def check_nulls(df,label):
    print("\n the number of null values:")
    print(df.isnull().sum())
    df.dropna(inplace= True)
    print("\nafter dropping all of the null values, check if there is any null values: in the {}\n".format(label))
    print(df.isnull().any())
###define plot_hist to plot a histogram for the second column in a data frame
def plot_hist(df,label):
    plt.hist(df.iloc[:,1])
    plt.title('the betting number for {} with the number of matches '.format(label))
    plt.show()

###definr a describe function to give a statistical description for a dataframe
def describe(df,label):
    print("describe the data of the {}".format(label))
    print(df.describe())

if __name__ =='__main__':

    num_rows()
    df_tuple = avg_odds()
    label =['home','Away','Draw']
    n = 0
    while n < 3:
        check_nulls(df_tuple[n],label[n])
        describe(df_tuple[n],label[n])
        plot_hist(df_tuple[n],label[n])
        n += 1
