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

type_of_run="ALL"
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
#print df['Author_num']

# Create a random variable (random forests work best with a random variable)
df['random'] = [random.random() for i in range(len(df))]

# REMOVE columns that are non-numeric and the target response variable 'author'
features = list(df.columns)
print features
# response
features.remove('author')
# strings
features.remove('title')
features.remove('poem')
features.remove('author_num')
features.remove('largest_word')
features.remove('poem_stress_list')
#
# HELP, data leak... :: is there a way to convert this list of comma-spearated numbers to something digestible...
#[0, 7, 6, 10, 9, 10, 8, 8, 5, 9, 10, 3, 9, 6, 0, 12, 7, 8, 6, 9, 8, 10, 9, 6, 0, 6, 8, 10, 6, 8, 9, 9, 7, 4, 0, 9, 7, 10, 6, 4, 6, 0, 9, 3, 8, 9, 6]
features.remove('words_per_line')
#  ['', '11011101', '111101', '1011010110101', '11101011101', '01011011101', '11110101'  .... ]
features.remove('poem_stress_list_no_punct')

# CONVERT the string numbers to int
for f in features:
    df[f]=df[[f]].astype(float)

# create a test and training set
x_train, x_test, y_train, y_test = train_test_split(df[features], df.author_num.values, test_size=0.4, random_state=123)
x, y = df[features], df.author_num.values

# CLASSIFIER
etclf = ExtraTreesClassifier(n_estimators=20)
etclf.fit(x_train, y_train)

scores = cross_val_score(etclf, x, y)
print scores.mean()

# Print Confusion Matrix
print metrics.confusion_matrix(etclf.predict(x_test), y_test)
print authors


""" OUTPUT #####################
/Users/jhave/anaconda/lib/python2.7/site-packages/sklearn/cross_validation.py:401: Warning: The least populated class in y has only 1 members, which is too few. The minimum number of labels for any class cannot be less than n_folds=3.
  % (min_labels, self.n_folds)), Warning)
0.671469386087
[[4 0 0 ..., 0 0 0]
 [0 0 0 ..., 0 0 0]
 [0 0 5 ..., 0 0 0]
 ..., 
 [0 0 0 ..., 1 0 0]
 [0 0 0 ..., 0 0 0]
 [0 0 0 ..., 0 0 0]]
 ####################  
 """

