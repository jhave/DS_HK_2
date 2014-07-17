#! /usr/bin/env python

"""

1. 
Load all html files in "bio" folder from poetryfoundation.org

2.
Parse the html using BeautifulSoup to extract bio and author

2.
Write to a single txt file for later import and incorporation into pipeline

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

DATA_DIR = "../../../../data/poetryFoundation/"   
HTML_DIR = "bio_"+type_of_run
JSON_PATH = DATA_DIR+'json/bios/'

json_fn = "poetryFoundation_JSON_BIOs_"+type_of_run+".txt"
json_fn_path = JSON_PATH+json_fn

txt_fn = type_of_run+"_poetryFoundation_BIO.txt"
txt_fn_path = DATA_DIR+txt_fn

WRITE_TXT_DIR="txt_bios_"+type_of_run+"/"
# CREATE dir
if not os.path.exists(DATA_DIR+WRITE_TXT_DIR):
    os.makedirs(DATA_DIR+WRITE_TXT_DIR)

try:
    if os.path.isfile(txt_fn_path):
            os.unlink(txt_fn_path)
except Exception, e:
        print e



html_cnt=0
txt_cnt=0
everything_string=""
ALL_titles=""

for root, subFolders, files in os.walk(DATA_DIR+HTML_DIR):

        for filename in files:

            filePath = os.path.join(root, filename)
            id = filename.split(".")[0]

            html_cnt=html_cnt+1

            author = ""
            bio = ""
            titles = ""

            print "\n"+id

            raw = open(filePath).read()  

            soup = BeautifulSoup(raw)
            
            bio = soup.find("div", { "class" : "biography" })
            
            author_div=soup.find("div", { "class" : "tabs-poet" })
 
            if bio is not None:

                txt_cnt += 1
                
                if author_div is not None:

                    author= author_div.find('a').text   

                    print "author:",author.encode('utf-8')

                    for em in bio.findAll('em'):
                        #print em
                        ALL_titles  += em.text +" !~*~! "
                        titles  += em.text +" !~*~! "
                        # print ALL_titles

                # collection
                everything_string += author.encode('utf-8')+"\n****!****\n"+titles.encode('utf-8')+"\n****!****\n"+bio.text.encode('utf-8')+"\n\n~~~~!~~~\n"

                # bio seperate
                f_txt=open(DATA_DIR+WRITE_TXT_DIR+id+".txt",'w')
                f_txt.write(author.encode('utf-8')+"\n****!****\n"+titles.encode('utf-8')+"\n****!****\n"+bio.text.encode('utf-8'))       
                f_txt.close();   
                print "WRITING TO:",WRITE_TXT_DIR+id+".txt"
                #print author.encode('utf-8')+"\n****!****\n"+titles.encode('utf-8')+"\n****!****\n"+bio.text.encode('utf-8')


# txt file for all scraped bios
f_txt=open(txt_fn_path,'w')
f_txt.write(everything_string)       
f_txt.close();    
print "\nTXT file created at:",txt_fn_path

txt_fn = type_of_run+"_poetryFoundation_BIO_ALL_TITLES.txt"
txt_fn_path = DATA_DIR+txt_fn
f_txt=open(txt_fn_path,'w')
f_txt.write(ALL_titles.encode('utf-8'))       
f_txt.close();   
print "\nTXT file created at:",txt_fn_path

#print everything_string

print "\n",html_cnt,"html files processed"
print txt_cnt,"poems sent to txt files"

print ALL_titles.encode('utf-8')


