#! /usr/bin/env python

"""

1. 
Load all html files in "poem" folder from poetryfoundation.org

2.
Parse the html using BeautifulSoup to extract features and labels

2.
Write in JSON format to a single txt file for later import and incorporation into pipeline
"""

import re

import os
import sys
import codecs


# for parsing html
from bs4 import BeautifulSoup

# for export of labels
import json



import pandas as pd 

# custom utilities....
import import_utilities

##############################################################
# NOTE: change HTML_DIR FOR TESTING
# EXAMPE USE: html_6 to test (because html_6 has only 6 files)
# change to 'html/' to scan all files
##############################################################

type_of_run="ALL"

HTML_DIR = "html_"+type_of_run

DIR = "../../../../data/poetryFoundation/"
WRITE_DIR = DIR+"txt_poems_"+type_of_run+"/"

if not os.path.exists(WRITE_DIR):
    os.makedirs(WRITE_DIR)

txt_fn = type_of_run+"_poetryFoundation_poems.txt"



html_cnt=0
txt_cnt=0
ALL_titles=""
ALL_poems=""

for root, subFolders, files in os.walk(DIR+HTML_DIR):



        for filename in files:
            
            filePath = os.path.join(root, filename)
            html_file_number = filename.split(".")[0]
            print html_file_number
            html_cnt=html_cnt+1

            poem_author = 'UNKNOWN'
            poem_title = 'UNKNOWN'
            poet_DOB = 'UNKNOWN'
            poem_dop = 'UNKNOWN'

            # HELP!!! get rid trouble characters NOT WORKING
            # UnicodeDecodeError: 'utf8' codec can't decode byte 0x80 in position 3131: invalid start byte
            #.decode('windows-1252')  #.decode('utf-8')

            raw = open(filePath).read()  
            #raw = codecs.open(filePath, encoding="ISO-8859-1").read()
           
            soup = BeautifulSoup(raw)
            
            poem = soup.find("div", { "class" : "poem" })
      
            if poem :

                pa = soup.select('span.author a')
                
                if pa:
                    poem_author = soup.select('span.author a')[-1].text.lstrip()
                    
                    title_id = soup.find(id="poem-top")

                    if (soup.select('span.author span.birthyear')):
                        poet_DOB = soup.select('span.author span.birthyear')[0].text
                    else:
                        poet_DOB = "0000"


                    poet_DOB = poet_DOB.encode('utf-8')
                    db = re.split("\xe2\x80\x93", poet_DOB)
                    if len(db)==2:
                        poet_DOB= db[0]+"-"+db[1]
                    #print poet_DOB

                    # if there is NO title, there is no poem
                    if title_id:

                        txt_cnt = txt_cnt+1

                        poem_title = title_id.find("h1").text
                        poem_title = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, poem_title)
                                        
                        #print 'Title:',poem_title.encode('utf-8')
                        ALL_titles=ALL_titles+", "+poem_title


                        # 
                        # all poem in one 
                        #

                        clean_poem = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, poem.text.encode('utf-8'))
                        ALL_poems= ALL_poems+poem_author.encode('utf-8')+"\n****!****\n"+poem_title.encode('utf-8')+"\n****!****\n"+clean_poem+"\n\n~~~~!~~~\n"



                        # 
                        # WRITE Poems to txt folder

                        txt_fn_single = html_file_number+".txt"
                        #print "TXT Filename: ", txt_fn.encode('utf-8')

                        
                        txt_fn_path = WRITE_DIR+txt_fn_single
                        
      

                        # TOTAL CHEAT "246708" is an anomaly in dataset...
                        if html_file_number != "247608":
                            f=open(txt_fn_path,'w')
                            
                            clean_poem = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, poem.text.encode('utf-8'))
                            
                            dp = poem_author.encode('utf-8')+"\n****!****\n"+poem_title.encode('utf-8')+"\n****!****\n"+clean_poem+"\n\n~~~~!~~~\n"
                            #print poem.text.encode('utf-8') #soup.prettify().encode('utf-8') #poem.html #.text.encode('utf-8')

                            f.write(dp)

                            f.close();

            
 

print html_cnt,"html files processed"
print txt_cnt,"poems sent to txt files"

txt_fn_path = DIR+txt_fn
f=open(txt_fn_path,'w+')
f.write(ALL_poems)
f.close();

print txt_fn_path
'''
10565 html files processed
10561 poems sent to txt files
json file created at: ../../../../data/poetryFoundation/json/poetryFoundation_JSON-COMPLETE.txt
[Finished in 1041.9s]
'''

