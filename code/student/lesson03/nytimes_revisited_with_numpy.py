#!/usr/bin/python
# Import required libraries
import numpy as np
import pandas as pd
import urllib

"""
The NYTimes data is hosted across 30 csv files:

We'd like to use Pandas and numpy to have a simple script that aggregates all of this data into one dataframe. This time, let's just get the click through rate per age, gender, and signed_in (remember that CTR is calculated as clicks/impressions).

You can export the final dataframe using pandas to_csv:
df.to_csv('nytimes_aggregation.csv')
"""

#
# GET NYT DATA  ::: RUN ONCE TO DOWNLOAD ::: THEN COMMENT OUT
#
""" initially tried to iterate thru & bash cmd curl 
to download the 30 nyt.csv files and stash them in data. 
....NOTE: an ! before curl allows it to run in ipython"""

""" USE import urllib TO get all the NYT csv data

for x in range(1, 31):
    
    nyt_url = "http://stat.columbia.edu/~rachel/datasets/nyt" + str(x) + ".csv"
    csv = "../../../data/lesson03/nytimes"+str(x)+".csv"


    impressions=urllib.URLopener()
    impressions.retrieve(nyt_url,csv)

     """

#
# MERGE  ::: RUN ONCE :::  THEN COMMENT
#
""" iterate thru all downloaded csv files
& MERGE them using pd.merger(df1,df2)
into single data frame
then write to a single csv
"""

""" THROWS AN out of memory ERROR...

#init the first csv as workaround....
df = pd.read_csv("../../../data/lesson03/nytimes1.csv")

for x in range(2, 3):
	csv = "../../../data/lesson03/nytimes"+str(x)+".csv"
	df1= pd.read_csv(csv)
	df2 = pd.merge(df1,df)

	print x
	print "df[:10]\n",df[:10]

df2.to_csv('nytimes_aggregation.csv')

"""



