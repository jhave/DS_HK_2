#!/usr/bin/env python

"""

USING the JSON file

1.
load pandas csv.

2.
do some plots.

3. 
try to figure out what the fuck is going on.

"""

from __future__ import division
from collections import Counter


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
# import dataframe (written during step 2) 
#

df = pd.read_csv(csv_PATH)
#print "DATAFRAME.head():\n",df.head(),"\n"

#  master_list.append(["id","author",'title','date_of_birth','date_of_death','date_of_publication','num_of_words','num_of_lines','num_of_verses','avg_word_len','avg_line_len','avg_lines_per_verse','longest_line','words_per_line','largest_word','poem'])

#
# plot 
#


# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


#
# access independent columns after sorting...
#

df.sort(['date_of_publication'],inplace=True)

df_subset = df.set_index('date_of_publication')


print df_subset[5:]
print "top # of words:\n",df.sort(['num_of_words']).head()

#print df_subset.describe()

# basic parameters
y_labl='Lines in poem'
x_labl='Year poem published'
colr='black'
fontsze=15
sze=1.2

fl = plt.figure(figsize=(16, 9) )

plt.ax = fl.add_subplot(111)
plt.ax.spines["top"].set_visible(False)
plt.ax.spines["bottom"].set_visible(False)
plt.ax.spines["right"].set_visible(False)
plt.ax.spines["left"].set_visible(False)
plt.ax.xaxis.label.set_color('black')
plt.ax.set_xlabel(x_labl, fontsize=fontsze)
plt.ax.set_ylabel(y_labl, fontsize=fontsze)
plt.ax.tick_params(axis='x', colors='black')
plt.ax.tick_params(axis='y', colors='black')
plt.ax.get_xaxis().tick_bottom()
plt.ax.get_yaxis().tick_left()
#
plt.text(0.2, 0.8,'# of LINES per poem', ha='center', va='center', transform=plt.ax.transAxes,fontsize=18, color='black')
plt.text(0.2, 0.7,'created from \npoetryfoundation.org \ncorpus of 10,576 poems \n(from year 1250 to 2014) ', ha='center', va='center', transform=plt.ax.transAxes,fontsize=14, color='black')
#plt.text(0.2, 0.5,'created from \npoetryfoundation.org \ncorpus of 10,576 poems \n(from year 1250 to 2014) ', ha='center', va='center', transform=plt.ax.transAxes,fontsize=15, color='black')
plt.ylim(0, 800)
plt.xlim(1250, 2020)
#sze = [1.00000001*n for n in df_subset['num_of_lines']]
plt.scatter(df_subset.index,df_subset['num_of_lines'],color=colr,s=sze)
plt.show()
#plt.savefig("img/plot_LINES.png")


# # LINES
# # plt.figure(figsize=(12, 9) )

# # # Remove the plot frame lines. They are unnecessary chartjunk.
# # plt.ax = plt.subplot(111)
# # plt.ax.spines["top"].set_visible(False)
# # plt.ax.spines["bottom"].set_visible(False)
# # plt.ax.spines["right"].set_visible(False)
# # plt.ax.spines["left"].set_visible(False)

# # # Ensure that the axis ticks only show up on the bottom and left of the plot.
# # # Ticks on the right and top of the plot are generally unnecessary chartjunk.
# # plt.ax.get_xaxis().tick_bottom()
# # plt.ax.get_yaxis().tick_left()








#    