# Investigate Soccer Database

## Preface: 

I will be using the soccer database which comes from Kaggle,this database contains data for more than 25,000 soccer matches,more than 10,000 players, and teams from several European countries from 2008 to 2016. 
 
## Preparing tools and the dataset: 
  I will be using the Anaconda environment to analyze the dataset, I have used  python scripts , I have created an environment for this investigation and I have exported it to soccer_investigate.yaml, you can import it to the local computer by using this command: 
 conda env create -f soccer_investigate.yaml   
you can run each script in the Anaconda Prompt using python word before each file name. 
you can download the dataset from this site: https://www.kaggle.com/hugomathien/soccer, 
 and Extract the zip file called "soccer.zip". 
 
## Posing questions: 

This analysis is answering on these important questions related to the soccer database: 

1.Which league has the most number of matches in all of the time period?

2.Is there a relashionship between the type of the team ( home, away) and the result of the match? 

3.Is there a relationship between the type of the team and the average betting number from diffrent companies? 

4.What teams improved the most over the time period? 

5.What team attributes  lead to the most vectories? 
 
## import libraries and Data collection: 

we will import these python libraries:sqlite3 for create a connection with the soccer database, Pandas and Numpy for data ingestion and manipulation, Matplotlib for Data visualization . 
To create the connection with the database ,we will use sqlite3.connect(path) function. 
 
1.we will perform the sql query by the pd.read_sql_query(query,conn) function in every investigation and store the result in a dataframe. 
2.in every plot  i have written plt.show() function to show the visualization, when the code is executed. 
3. in every use for the year, i have used substr(date,1,4) function to take the first four characters which are the year number, that sqlite doesn't have a convert function to date and time. 
