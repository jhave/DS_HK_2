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
from pandas import read_json

from sklearn.cross_validation import train_test_split
from sklearn.ensemble.forest import ExtraTreesClassifier
from sklearn import metrics
from sklearn import preprocessing

# Fit Model
from sklearn.cross_validation import cross_val_score

############

type_of_run="ALL"
DATA_DIR  =  "../../../../data/poetryFoundation/"

csv_fn="output_"+type_of_run+".csv"
csv_PATH = DATA_DIR+csv_fn

json_PATH=DATA_DIR+"json/STEP2_poetryFoundation_JSON_"+type_of_run+".txt"

############


import csv
import pandas as pd 
import numpy as np 
from numpy import nan
import matplotlib.pyplot as plt 

#
# import dataframe (output_ALL.csv written during step 2) 
#

# CSV df = pd.read_csv(csv_PATH)
# JSON
#####  FUNDAMENTAL orient="records" uses first record as header
df = pd.read_json(json_PATH, orient="records")

print "DATAFRAME.head():\n",df.head(),"\n"

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
print len(df),"FEATURES:\n",features
#print features

# REMOVE from input...
# response
features.remove('author')
# strings 
features.remove('title')
#features.remove('poem')
features.remove('author_num')
features.remove('largest_word')
#features.remove('poem_stress_list')
features.remove('words_per_line')
features.remove('chars_per_line')
#features.remove('poem_stress_list_no_punct')

# 1. CONVERT the string numbers to float
for f in features:
	#print f
	df[f]=df[[f]].astype(float)

# 2. FILL EMPTY SLOTS WITH ZEROES
dfeatures = df.fillna(0)


#print ",dfeatures[features][:-1]\n",dfeatures[features][:-1]
pd.set_option('display.max_columns', None)
print "ALL columns of dfeatures[features]"
print dfeatures[features].head(1)

# create a test and training set
x_train, x_test, y_train, y_test = train_test_split(dfeatures[features], dfeatures.author_num.values, test_size=0.4, random_state=123)
x, y = dfeatures[features], dfeatures.author_num.values

# CLASSIFIER
etclf = ExtraTreesClassifier(n_estimators=20)
etclf.fit(x_train, y_train)

scores = cross_val_score(etclf, x, y)
print scores.mean()

# Print Confusion Matrix
print metrics.confusion_matrix(etclf.predict(x_test), y_test)
# print authors

"""
# # PREVIOUS RESULT 0.671469386087

############# RESULT WITH ALL FEATURES ############
/Users/jhave/anaconda/lib/python2.7/site-packages/sklearn/cross_validation.py:401: Warning: The least populated class in y has only 1 members, which is too few. The minimum number of labels for any class cannot be less than n_folds=3.
  % (min_labels, self.n_folds)), Warning)
0.148101533384
[[0 0 0 ..., 0 0 0]
 [0 0 0 ..., 0 0 0]
 [0 0 0 ..., 0 0 0]
 ..., 
 [0 0 0 ..., 2 0 0]
 [0 0 0 ..., 0 0 0]
 [0 0 0 ..., 0 0 0]]
[Finished in 259.1s]
############################
"""