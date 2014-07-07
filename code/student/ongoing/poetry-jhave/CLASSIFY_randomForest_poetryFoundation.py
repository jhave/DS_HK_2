#!/usr/bin/env python

"""

1.
load pandas csv.

2.
do something with random forests based on ga class notebook
http://nbviewer.ipython.org/github/ga-students/DS_HK_2/blob/gh-pages/notebooks/14%20-%20Random%20Forests.ipynb

3. 
try to figure out what the fuck is going on.

"""

import random
from pandas import read_csv
from sklearn.cross_validation import train_test_split
from sklearn.ensemble.forest import ExtraTreesClassifier
from sklearn import metrics
from sklearn import preprocessing

# Fit Model
from sklearn.cross_validation import cross_val_score

############

type_of_run="6"
DATA_DIR  =  "../../../../data/poetryFoundation/"
csv_fn="output_"+type_of_run+".csv"
csv_PATH = DATA_DIR+csv_fn

############


import csv
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


#
# import dataframe (output_ALL.csv written during step 2) 
#

df = pd.read_csv(csv_PATH)
#print "DATAFRAME.head():\n",df.head(),"\n"

#
# preprocess : convert author names into numeric data
#

authors = list(set(df.author.values))
#print authors
le = preprocessing.LabelEncoder()
le.fit(authors)
df['author_num'] = le.transform(df['author'])

# Create a random variable (random forests work best with a random variable)
df['random'] = [random.random() for i in range(len(df))]

# REMOVE columns that are non-numeric and the target response variable 'author'
features = list(df.columns)
#print features

# REMOVE from input...
# response
features.remove('author')
# strings 
features.remove('title')
features.remove('poem')
features.remove('author_num')
# convert
features.remove('largest_word')
for lw in df['largest_word']:
    #print len(lw),lw
    df['largest_word_length']=len(lw)

# remove this one because the stress list also exists with "...no_punct" 
features.remove('poem_stress_list')

# # convert [0, 7, 6, 10, 9, 10, 8, 8, 5, 9, 10, 3, 9, 6, 0, 12, 7, 8, 6, 9, 8, 10, 9, 6, 0, 6, 8, 10, 6, 8, 9, 9, 7, 4, 0, 9, 7, 10, 6, 4, 6, 0, 9, 3, 8, 9, 6]
features.remove('words_per_line')


#
# deal with the stupidity of having put list into csv so it came back as a string
# thanks mart!
#

tmp=[]
for wpl in df['words_per_line'].values:
	wi = 0
	tmp.append([int(y) for y in filter(lambda a: a not in [' ',',','[',']'], wpl)])
	

print "TMP:",tmp
for ti in tmp:
	for t in ti:
		print ti.index(t),t

#find line with max # of lines
mx=0
for ti in tmp:
	#print len(ti),ti
	if len(ti)>mx:
		mx=len(ti)

# # create a column for each 
for i in range(mx):
    df['line_'+str(i)]=0

# put values in 
# for ti in tmp:
# 	print tmp.index(ti)
	#for t in ti:
		#df['words_per_line']=
		#print ti.index(t),t


#print list(df.columns)



# 	# df['line_'+str(i)]
# 	# i += 1

# 
    # wcnt=0
    # for idx,ws in enumerate(wpl):
    #     if ws.isdigit():
    #         #print idx,ws
    #         df['ln'+str(wcnt)]=ws
    #         wcnt+=1
        #else:
        	#print ws



#  ['', '11011101', '111101', '1011010110101', '11101011101', '01011011101', '11110101'  .... ]
features.remove('poem_stress_list_no_punct')
# for pslp in df['poem_stress_list_no_punct']:
#     #print len(pslp),pslp
#     for idx,ps in enumerate(wpl):
#         if ps.isdigit():
#             #print idx,ps
#             df['stress'+str(idx)]=ps


# # FILL EMPTY SLOTS WITH ZEROES
df.fillna(0)

# #df.tail()


# # CONVERT the string numbers to int
# for f in features:
#     df[f]=df[[f]].astype(float)

# # create a test and training set
# x_train, x_test, y_train, y_test = train_test_split(df[features], df.author_num.values, test_size=0.4, random_state=123)
# x, y = df[features], df.author_num.values

# # CLASSIFIER
# etclf = ExtraTreesClassifier(n_estimators=20)
# etclf.fit(x_train, y_train)

# scores = cross_val_score(etclf, x, y)
# print scores.mean()

# # Print Confusion Matrix
# print metrics.confusion_matrix(etclf.predict(x_test), y_test)
# # print authors


# # 0.671469386087