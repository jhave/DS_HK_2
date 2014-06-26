#! /usr/bin/env python

"""

1. 
Parse the html using BeautifulSoup

2.
For each html file: 

    Write metadata to JSON file json folder: file #, Author, Title, date of publication, birthyear of author, ... [HELP! LABELS : not working, need help parsing them....]

    Write poem to TXT file in txt folder.


NOTE: due to a parsing error (its impossible to remove some of the spaces) in the next step "loading_JSON.py" -- there might be a bug in write encoding of the poem txt file.

"""

import re

import os
import sys


# for parsing html
from bs4 import BeautifulSoup

# for export of labels
import json

DIR = "../../../../data/poetryFoundation/"



import pandas as pd 




##############################################################
# NOTE: change HTML_DIR FOR TESTING
# EXAMPE USE: html_6 to test (because html_6 has only 6 files)
# change to 'html/' to scan all files
##############################################################

JSON_PATH = DIR+'json/'   
HTML_DIR = "html_6/"
json_fn = "poetryFoundation_JSON_6.txt"

json_fn_path = JSON_PATH+json_fn

try:
    if os.path.isfile(json_fn_path):
            os.unlink(json_fn_path)
except Exception, e:
        print e


# JSON file
f_json=open(json_fn_path,'a')


for root, subFolders, files in os.walk(DIR+HTML_DIR):

        html_cnt=0
        txt_cnt=0

        for filename in files:
            
            filePath = os.path.join(root, filename)
            html_file_number = filename.split(".")[0]
            print html_file_number
            html_cnt=html_cnt+1
            
            soup = BeautifulSoup(open(filePath))
            
            poem = soup.find("div", { "class" : "poem" })
            
            if poem:
                
                pa = soup.select('span.author a')
                
                if pa:
                    poem_author = soup.select('span.author a')[0].text
                    #print 'Author:',poem_author.encode('utf-8')
                    title_id = soup.find(id="poem-top")

                    if (soup.select('span.author span.birthyear')):
                        #poet_DOB, poet_DOD = clean_life(soup.select('span.author span.birthyear')[0].text)
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
                        #print 'Title:',poem_title.encode('utf-8')

                        # poem_dop == date of publication
                        poem_dop=''
                        credits = soup.find('div', attrs={'class' : 'credit'})
                        if credits:

                            pcred = credits.find("p").text
                            credits=unicode.join(u'\n',map(unicode,credits))
                          
                            #
                            # different formatting of dop
                            #
                            if pcred.find("Copyright")>0 & pcred.find("Source")<0:
                                #print "found copyright"
                                poem_dop = pcred[(pcred.find("Copyright")+12):(pcred.find("Copyright")+16)]
                            elif pcred.find("@")>0:
                                #print "found @"
                                poem_dop = pcred[(pcred.find("@")+1):(pcred.find("@")+5)]
                            else:
                                #print "found SOURCE:",credits.encode('utf-8')
                                if credits.rfind(")")>0:
                                    #print "found )"
                                    poem_dop=credits[(credits.rfind(")")-4):(credits.rfind(")")-0)]
                                elif credits.encode('utf-8').rfind("\xc2")>0:
                                    #print "find cop",credits.encode('utf-8').rfind("\xc2")
                                    poem_dop=credits[(credits.encode('utf-8').rfind("\xc2")+1):(credits.encode('utf-8').rfind("\xc2")+5)]
                                else:
                                    #print "no dop"
                                    #... cld b cheated with poet_DOB+25
                                    poem_dop =''
                      
                                # catch errors(many old poems have no dop)
                                if poem_dop.isdigit() == False:
                                    poem_dop=''

                            #print "dop:",poem_dop.encode('utf-8')
                           

                       # NOTE: features are stored here
                       # in this dict that holds lists of labels
                        categories = {}
                        # labels are all within 'about' div
                        about = soup.find('div', attrs={'class' : 'about'})
                        # nested within their own section
                        
                        #print "magazing entries have no labels:",about
                        if about != None:
                            ps_about = about.find_all('p', attrs={'class' : 'section'})

                            for slug in ps_about:
                                labels = slug.find('span', attrs={'class' : 'slug'})

                                if labels.text  != 'Poet':
                                    
                                    category = labels.text    
                                    #print category.encode('utf-8'), ": "

                                    # create a list within dict for this category
                                    categories[category] = []

                                    lbs = labels.find_next_siblings()

                                    for lb in lbs:
                                        categories[category].append(lb.text)

                                    # for cat_label in categories[category]:
                                        # print cat_label.encode('utf-8')

                            print categories


              
                        # JSON write to json folder
                        # MOVED f_json=open(json_fn_path,'a')
                    
                       # print html_file_number.encode('utf-8'), '   Author', poem_author.encode('utf-8').lstrip() ,'   Title' , poem_title.encode('utf-8')


                        # Example Structur
                        # {
                        # "id" : 8,
                        # "Author": "Averill  Curdy",
                        # "Title": "Probation",
                        # "poet_DOB": "0000",
                        # "poem_dop": "2005",
                        # "labels" : ['hellow', 'world']
                        # "text": ""
                        # },

                        # json.dump([html_file_number.encode('utf-8'), { 'Author': poem_author.encode('utf-8').lstrip() } , { 'Title' : poem_title.encode('utf-8') }  , { 'poet_DOB' : poet_DOB} , {'poem_dop' : poem_dop.encode('utf-8')} ], f_json)
                        json.dump({ 'id': html_file_number.encode('utf-8'), 'author': poem_author.encode('utf-8').lstrip(), 'title' : poem_title.encode('utf-8'), 'poet_DOB' : poet_DOB, 'poem_dop' : poem_dop.encode('utf-8'), 'labels' : categories, 'poem' : poem.text.encode('utf-8') }, f_json)
                      
                        # 
                        # PANDAS
                        #



                        

                        # NOTE: 
                        # assert isinstance(poem, str)    
                        # AssertionError Why????


                        # WRITE Poems to txt folder
                        txt_fn = html_file_number+".txt"
                        #print "TXT Filename: ", txt_fn.encode('utf-8')

                        dir = DIR+'txt'
                        txt_fn_path = dir+"/"+txt_fn
                        # print "TXT Path/Filename: ",txt_fn_path.encode('utf-8')
                        f=open(txt_fn_path,'w+')

                        # REMOVED f.write(poem.text.encode('utf-8').strip())

                        dp = poem.text.encode('utf-8')
                        f.write(dp)

                        f.close();

            
f_json.close();    

print html_cnt,"html files processed"
print txt_cnt,"poems sent to txt files"
print "json file created at:",json_fn_path


def clean_life(str):
    # change it  to split and clean the data.... get rid of apostrophe elsewhere
    dob,dod=str,str
    return dob, dod

"""
******************************************
3011 html files processed
2988 poems sent to txt files
json file created at: ../../../../data/poetryFoundation/json/poetryFoundation_JSON.txt
[Finished in 390.3s]
******************************************
"""