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
# import dataframe (output_ALL.csv written during step 2) 
#

df = pd.read_csv(csv_PATH)
# print "DATAFRAME.head():\n",df.head(),"\n"

#
# DATA WRANGLE : sorting, set-index 
#

df.sort(['date_of_publication'],inplace=True)

df_subset = df.set_index('date_of_publication')
# print df_subset[5:]
#print "\ntop # of words:\n",df.sort(['num_of_words']).head()
# print df_subset.describe()
#print "MAX num_of_lines:",df['num_of_lines'].max()
print "MAX avg_word_len:",df['avg_word_len'].max()
# print "Most LINES:"
#print df[['date_of_publication', 'author', 'title','num_of_lines']].sort(['num_of_lines']).tail(20)
#
# pretty plot parameters from http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
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
#  PLOTTING ALONG by iterating thru and plotting everything against date of publication at various ranges
#
individual_label_limit_LINES=250
individual_label_limit_WORDS=2000
individual_label_limit_VERSES=50

individual_label_limit_Avg_LINE_Length=50
individual_label_limit_Avg_WORD_Length=5

#["id","author",'title','date_of_birth','date_of_death','date_of_publication','num_of_words','num_of_lines','num_of_verses','avg_word_len','avg_line_len','avg_lines_per_verse','longest_line','words_per_line','largest_word','poem','poem_stress_list','poem_stress_list_no_punct'])

#plot_stuff = [{"begin_year":0,"end_year":2015,"img_title":'# of LINES','individual_label_limit':300,"xvar":'num_of_lines'},{"begin_year":1250,"end_year":2015,"img_title":'# of LINES','individual_label_limit':300,"xvar":'num_of_lines'},{"begin_year":1900,"end_year":2015,"img_title":'# of LINES','individual_label_limit':300,"xvar":'num_of_lines'},{"begin_year":1970,"end_year":2015,"img_title":'# of LINES','individual_label_limit':300,"xvar":'num_of_lines'},{"begin_year":2000,"end_year":2015,"img_title":'# of LINES','individual_label_limit':300,"xvar":'num_of_lines'},{"begin_year":0,"end_year":2015,"img_title":'# of WORDS','individual_label_limit':individual_label_limit_WORDS,"xvar":'num_of_words'},{"begin_year":1250,"end_year":2015,"img_title":'# of WORDS','individual_label_limit':individual_label_limit_WORDS,"xvar":'num_of_words'},{"begin_year":1900,"end_year":2015,"img_title":'# of WORDS','individual_label_limit':individual_label_limit_WORDS,"xvar":'num_of_words'},{"begin_year":1970,"end_year":2015,"img_title":'# of WORDS','individual_label_limit':individual_label_limit_WORDS,"xvar":'num_of_words'},{"begin_year":2000,"end_year":2015,"img_title":'# of WORDS','individual_label_limit':individual_label_limit_WORDS,"xvar":'num_of_words'},{"begin_year":0,"end_year":2015,"img_title":'# of VERSES','individual_label_limit':individual_label_limit_VERSES,"xvar":'num_of_verses'},{"begin_year":1250,"end_year":2015,"img_title":'# of VERSES','individual_label_limit':individual_label_limit_VERSES,"xvar":'num_of_verses'},{"begin_year":1900,"end_year":2015,"img_title":'# of VERSES','individual_label_limit':individual_label_limit_VERSES,"xvar":'num_of_verses'},{"begin_year":1970,"end_year":2015,"img_title":'# of VERSES','individual_label_limit':individual_label_limit_VERSES,"xvar":'num_of_verses'},{"begin_year":2000,"end_year":2015,"img_title":'# of VERSES','individual_label_limit':individual_label_limit_VERSES,"xvar":'num_of_verses'}]

#plot_stuff=[{"begin_year":0,"end_year":2015,"img_title":'Average LINE Length','individual_label_limit':individual_label_limit_Avg_LINE_Length,"xvar":'avg_line_len'},{"begin_year":1250,"end_year":2015,"img_title":'Average LINE Length','individual_label_limit':individual_label_limit_Avg_LINE_Length,"xvar":'avg_line_len'},{"begin_year":1900,"end_year":2015,"img_title":'Average LINE Length','individual_label_limit':individual_label_limit_Avg_LINE_Length,"xvar":'avg_line_len'},{"begin_year":1970,"end_year":2015,"img_title":'Average LINE Length','individual_label_limit':individual_label_limit_Avg_LINE_Length,"xvar":'avg_line_len'},{"begin_year":2000,"end_year":2015,"img_title":'Average LINE Length','individual_label_limit':individual_label_limit_Avg_LINE_Length,"xvar":'avg_line_len'}]


plot_stuff=[{"begin_year":0,"end_year":2015,"img_title":'Average WORD Length','individual_label_limit':individual_label_limit_Avg_WORD_Length,"xvar":'avg_word_len'},{"begin_year":1250,"end_year":2015,"img_title":'Average WORD Length','individual_label_limit':individual_label_limit_Avg_WORD_Length,"xvar":'avg_word_len'},{"begin_year":1900,"end_year":2015,"img_title":'Average WORD Length','individual_label_limit':individual_label_limit_Avg_WORD_Length,"xvar":'avg_word_len'},{"begin_year":1970,"end_year":2015,"img_title":'Average WORD Length','individual_label_limit':individual_label_limit_Avg_WORD_Length,"xvar":'avg_word_len'},{"begin_year":2000,"end_year":2015,"img_title":'Average WORD Length','individual_label_limit':individual_label_limit_Avg_WORD_Length,"xvar":'avg_word_len'}]

for ps in plot_stuff:
#     print "ps['begin_year']:",ps['begin_year']

    # basics
    img_title = ps['img_title']
    individual_label_limit=ps['individual_label_limit']
    y_labl=img_title+' in poem'
    x_labl='Date of publication'
    colr='black'
    fontsze=16
    sze=1.3

    begin_year= ps['begin_year'] #1250
    end_year= ps['end_year'] #2015
    xvar= ps['xvar'] #'num_of_lines'

    df_ranged= df[(df.date_of_publication > begin_year) & (df.date_of_publication < end_year)]
    total_poems_used=len(df_ranged.index)
    ylimt = df[xvar].max()
    print "ylimt:",ylimt
    print "total_poems_used in range from :", total_poems_used
    print '\n'


    credits_txt=str(total_poems_used)+' poems scraped\nfrom poetryfoundation.org \nanalyzed with python'

    fl = plt.figure(figsize=(16, 9) )

    plt.ax = fl.add_subplot(111)
    plt.ax.spines["top"].set_visible(False)
    #plt.ax.spines["bottom"].set_visible(False)
    plt.ax.spines["right"].set_visible(False)
    #plt.ax.spines["left"].set_visible(False)
    plt.ax.xaxis.label.set_color('black')
    plt.ax.set_xlabel(x_labl, fontsize=fontsze, labelpad = 5)
    plt.ax.set_ylabel(y_labl, fontsize=fontsze, labelpad = 10)
    plt.ax.tick_params(axis='x', colors='black',direction=50)
    plt.ax.tick_params(axis='y', colors='black')
    plt.xticks(rotation=40)
    plt.ax.get_xaxis().tick_bottom()
    plt.ax.get_yaxis().tick_left()
    #
    plt.text(0.2, 0.85,img_title+' per poem\nYears: '+str(begin_year)+' to '+str(end_year), ha='center', va='center', transform=plt.ax.transAxes,fontsize=18, color='black', weight='bold')
    plt.text(0.2, 0.75,credits_txt, ha='center', va='center', transform=plt.ax.transAxes,fontsize=14, color='black')
    #
    plt.ylim(0, ylimt)
    plt.xlim(begin_year, end_year)
    #
    plt.scatter(df_subset.index,df_subset[xvar],color=colr,s=sze)

    for label, x, y in zip(df_subset['author'], df_subset.index,df_subset[xvar]):
        if xvar is not 'avg_word_len':
            if y>individual_label_limit:
                print "y:",y
                plt.annotate(
                    label.decode('utf-8'), 
                    xy = (x, y), xytext = (-20, 20),
                    textcoords = 'offset points', ha = 'left', va = 'bottom',
                    bbox = dict(boxstyle = 'square,pad=0.5', fc = 'white', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', 
                                        connectionstyle='arc3,rad=-0.3'))
        else:
            if y>individual_label_limit or y<3:
                print "y:",y
                plt.annotate(
                    label.decode('utf-8'), 
                    xy = (x, y), xytext = (-20, 20),
                    textcoords = 'offset points', ha = 'left', va = 'bottom',
                    bbox = dict(boxstyle = 'square,pad=0.5', fc = 'white', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', 
                                        connectionstyle='arc3,rad=-0.3'))  

    #plt.show()
    plt.savefig('img/plot_'+img_title+'_'+str(begin_year)+'_'+str(end_year)+'.png', dpi=120)

# END LINES
