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

type_of_run="60"
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

#df = pd.read_csv(csv_PATH)
df = pd.read_json(json_PATH)
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
print len(df)
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
features.remove('poem_stress_list_no_punct')


# 1. CONVERT the string numbers to float
for f in features:
	#print f
	df[f]=df[[f]].astype(float)

# 2. FILL EMPTY SLOTS WITH ZEROES
dfeatures = df.fillna(0)


print "DFeatures tail()\n",dfeatures.head()


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


# # 0.671469386087