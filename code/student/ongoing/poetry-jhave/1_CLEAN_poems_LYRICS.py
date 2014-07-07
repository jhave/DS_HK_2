#! /usr/bin/env python

"""

1. 
Load all html.txt files in "poem" folder from ohhla.com

2.
Parse the html using BeautifulSoup to extract features and labels

2.
Write in JSON format to a single txt file for later import and incorporation into pipeline

"""
from __future__ import division
from collections import Counter

import nltk, re, pprint
from nltk import Text
from nltk.corpus import cmudict
from nltk.tokenize import WhitespaceTokenizer

import re

import os
import sys
import collections


# for parsing html
from bs4 import BeautifulSoup

# for export of labels
import json
import pandas as pd 


##############################################################
#\
type_of_run="6"  # "60" "ALL"
DIR = "../../../../data/poetry/lyrics/"
DATA_DIR = "../../../../data/poetry/lyrics/en_txt/"
WRITE_DIR = "../../../../data/poetry/lyrics/en_seperate_songs/"
txt_fn="lyrics"

JSON_PATH = DIR+'json/'   
json_fn = "poetryFoundation_JSON_"+type_of_run+".txt"
json_fn_path = JSON_PATH+json_fn

try:
    if os.path.isfile(json_fn_path):
            os.unlink(json_fn_path)
except Exception, e:
        print e


# JSON file
f_json=open(json_fn_path,'a')



cnt=0
for root, subFolders, files in os.walk(DATA_DIR):
    #print root


    for filename in files:

            if '.txt' in filename:
                cnt=cnt+1


                filePath = os.path.join(root, filename)

                raw = open(filePath).read() 
                
                artistName = filename.split('-')[0]
                artistName = artistName.rstrip()

                # correction of filename:   BEATLES (THE)
                if artistName.split()[-1]=="The":
                    first = artistName.rsplit(' ',1)[0]
                    last = artistName.split()[-1]
                    artistName = last+' '+first


                songs = raw.split(artistName.upper())

                #if artistName=="U2":

                print "\n\n************\nartistName.upper(): '"+artistName.upper()+"'     filename:",filename,"len(songs)",len(songs),"\n************\n"

                song_list=[]

                cnt =0

                for song in songs:
                    lines = song.split("\n")
                    title = lines[1].title().strip(' \t\n\r').rstrip().lstrip()
                    title = ' '.join(title.split())


                    if len(title)>1: 
                        #print cnt,"title: '"+title+"'"
                        id = artistName+'_'+title
                        song_list.append({ 'title':title, 'author':artistName, 'poem':"\n".join(lines[2:]),'len':len("\n".join(lines[2:])) })
                        cnt+=1

                print len(song_list)

                # # remove duplicate versions of same song by taking only longest
                data = collections.defaultdict(list)

                for i in song_list:
                    # if  len(i['title'].split("("))>1:
                    #     i['title']
                    data[i['title']].append(i['len'])
                    #data[i['title']].append(i['song'])
                
                output = [{'title': i, 'len': max(j)} for i,j in data.items()]

                song_list_pruned=[]
                print len(output)
                for o in output:
                    #print output.index(o),o['title'],o['len']
                    for sd in song_list:
                        if sd['title']==o['title']:
                            if sd['len']==o['len']:
                                #print "INCLUDE"
                                # prune the duplicate entry
                                song_list_pruned.append({'title':sd['title'],'poem': sd['poem'] , 'author':sd['author'], 'len': sd['len']  })




                    # SAVE EACH SONG AS TXT FILE
                    # print len(song_list_pruned)
                    # for slp in song_list_pruned:
                    #     txt_fn_path =WRITE_DIR+slp['author']+'_'+slp['title']
                    #     f=open(txt_fn_path,'w+')
                    #     clean_poem = slp['poem'].encode('utf-8')
                    #     dp = clean_poem
                    #     f.write(dp)
                    #     f.close();
                    #     print slp['id'], slp['title'],slp['author'],slp['poem'].split("\n")[1]

                    # write a text file

                    # JSON dump returns out of range ascii error 
                    for slp in song_list_pruned:
                        json.dump(slp, f_json)
                      



            
f_json.close();    





