#!/usr/bin/python
# Import required libraries
import numpy as np
import pandas as pd

# Set some Pandas options
pd.set_option('max_columns', 30)
pd.set_option('max_rows', 20)

# Store data in a consistent place

DATA_DIR = '../../../data/'


# Import the Aggregated NTY data we built up in Lesson 

df = pd.read_csv(DATA_DIR + 'baseball.csv')
#print df[:10]

#show count, mean, std, min, 25%...max for each column
#print df.describe()

#change index WITHIN current DataFrame
#df.set_index('id', inplace=True)
#show first 5 lines
#print df.head()

#show count, mean, std, min, 25%...max for each column NOW excludes id column because it is index
#print df.describe()


"""
Notice that we've lost the default pandas 0-based index and moved the user_id into its place. We can select rows based on the index using the ix method
BUT these would need to be set to 3 existing numbers....

print df.ix[99]
print 'then print 3 users \n'
print df.ix[[1, 50, 100]]
"""

# max homerun array  ????
# max_hr = df.sort('hr', ascending=False).head()
# print "max_hr:",max_hr

""" ROUGH STRATEGY 

isolate the following 
with the weights

H Hits				*   1
X2B Doubles			*	2
X3B Triples     	*	3
R Runs 				*	4
HR Homeruns			*	5
RBI Runs Batted in 	* 	1

sum them?
do an inner join?

"""

# make a copy
baseball = df.copy()


# h
h = baseball.sort('h',ascending=False).head()
print "Hits top 5:\n",h['h']

# X2B
X2b = baseball.sort('X2b',ascending=False).head()
print "\nX2B top 5:\n",X2b['X2b']

# X3B
X3b = baseball.sort('X3b',ascending=False).head()
print "\nX3B top 5:\n",X3b['X3b']

# r
r = baseball.sort('r',ascending=False).head()
print "\nr top 5:\n",r['r']

# homeruns
hr = baseball.sort('hr',ascending=False).head()
print "\nHomerun top 5:\n",hr['hr']

# rbi
rbi = baseball.sort('rbi',ascending=False).head()
print "\nrbi top 5:\n",rbi['rbi']

##
##normalize the dataset
##

