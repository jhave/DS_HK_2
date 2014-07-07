#! /usr/bin/env python

"""

1. 
Load all html.txt files in "poem" folder from ohhla.com

2.
Parse the html using BeautifulSoup to extract features and labels

2.
Write in JSON format to a single txt file for later import and incorporation into pipeline

"""

import re

import os
import sys


# for parsing html
from bs4 import BeautifulSoup

# for export of labels
import json
import pandas as pd 


##############################################################
#
DATA_DIR = "../../../../data/poetry/lyrics/en_txt/"
WRITE_DIR = "../../../../data/poetry/lyrics/analysis/"

txt_fn="lyrics"

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

                if artistName=="U2":

                    print "\n\n************\nartistName.upper(): '"+artistName.upper()+"'     filename:",filename,"len(songs)",len(songs),"\n************\n"

                    song_dict=[]

                    cnt =0

                    for song in songs:
                        lines = song.split("\n")
                        title = lines[1].title().strip(' \t\n\r').rstrip().lstrip()
                        title = ' '.join(title.split())


                        if len(title)>1: 
                            #print cnt,"title: '"+title+"'"
                            song_dict.append({'title':title,'song':"\n".join(lines[2:]),'len':len("\n".join(lines[2:])) })
                            cnt+=1

                    print len(song_dict)

                    # # remove duplicate versions of same song by taking only longest
                    # for sd in song_dict:
                    #     for sd2 in song_dict:
                    #         if sd['title'] == sd2['title'] and song_dict.index(sd) != song_dict.index(sd2):#.split('(')[0]: 
                    #             print song_dict.index(sd),song_dict.index(sd2),"DUPLICATE:",sd['title'],"    &    ",sd2['title']
                    #             if sd['len']>len(sd2['song']):


                        #print "title:",sd['title'],"len(sd['song']):",len(sd['song'])#,"\n",sd['song']

                    





                # if (soup.pre is None) or (len(soup.pre) == 0):
                #     print "None"
                # else:
                #     htm = url
                #     htm +=soup.pre.text
                #     txt_fn_path = WRITE_DIR+filename
                #     print "WRITE: ",txt_fn_path


                #     if not os.path.exists(WRITE_DIR):
                #         os.makedirs(WRITE_DIR)
                   
                #     f=open(txt_fn_path,'w+')
                #     f.write(htm.encode('utf-8'))
                #     f.close();

        