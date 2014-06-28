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


# for parsing html
from bs4 import BeautifulSoup

# for export of labels
import json

DIR = "../../../../data/poetryFoundation/"

import pandas as pd 

# remove annoying characters
chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : '' ,        # modifier - under line
    '\xe2\x80\x99': '\'',   # apostrophe
    '\xe2\x80\x94': '--'    # em dash

}


# USAGE new_str = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, text)
def replace_chars(match):
    char = match.group(0)
    return chars[char]



##############################################################
# NOTE: change HTML_DIR FOR TESTING
# EXAMPE USE: html_6 to test (because html_6 has only 6 files)
# change to 'html/' to scan all files
##############################################################

JSON_PATH = DIR+'json/'   
HTML_DIR = "html_60"
json_fn = "poetryFoundation_JSON-COMPLETE_60.txt"

json_fn_path = JSON_PATH+json_fn

try:
    if os.path.isfile(json_fn_path):
            os.unlink(json_fn_path)
except Exception, e:
        print e


# JSON file
f_json=open(json_fn_path,'a')

html_cnt=0
txt_cnt=0

for root, subFolders, files in os.walk(DIR+HTML_DIR):



        for filename in files:
            
            filePath = os.path.join(root, filename)
            html_file_number = filename.split(".")[0]
            print html_file_number
            html_cnt=html_cnt+1
            

            # HELP!!! get rid trouble characters NOT WORKING
            # UnicodeDecodeError: 'utf8' codec can't decode byte 0x80 in position 3131: invalid start byte
            raw = open(filePath).read()  #.decode('windows-1252')  #.decode('utf-8')
            #original = raw.decode('utf-8')
            #raw = unicode(raw, "utf-8")
            #replacement = raw.replace(u"\u201c", '"')#.replace(u'\u201d', '"').replace(u'\u2019', "'")
            soup = BeautifulSoup(raw)

            #print "LOOOOKING for u to replace inside soup:"
            # ustuff = soup.find_all(text= re.compile(u'\u201d'))
            # for us in ustuff:
            #     print "us:",us
            #     us.replace_with(new_tag)
            
            poem = soup.find("div", { "class" : "poem" })
            
            if poem:
                #print "ok"

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
                        print 'Title:',poem_title.encode('utf-8')

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
                                    poem_dop ='0000'
                      
                                # catch errors(many old poems have no dop)
                                if poem_dop.isdigit() == False:
                                    poem_dop='0000'
                                elif poem_dop=='':
                                    poem_dop='0000'

                            #print "dop:",poem_dop.encode('utf-8')
                           

                       # NOTE: features are stored here
                       # in this dict that holds lists of labels
                        categories = {}
                        # labels are all within 'about' div
                        about = soup.find('div', attrs={'class' : 'about'})
                        # nested within their own section
                        
                        #print "entries have no labels:",about
                        if about != None:
                            ps_about = about.find_all('p', attrs={'class' : 'section'})

                            for slug in ps_about:
                                labels = slug.find('span', attrs={'class' : 'slug'})

                                if labels.text  != 'Poet':
                                    
                                    #labels.text.replace(u'\u2019', "'")
                                    category = labels.text
                                    #new_label = "category_"+ labels.text   
                                    #print category.encode('utf-8'), ": "
                                    clean_cat = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, category.encode('utf-8'))
                                    print "clean_cat:",clean_cat
                                    if "REGION" in clean_cat:
                                        clean_cat = "Region"
                                        print "CLEANED category:", clean_cat
                                   

                                    # create a list within dict for this category
                                    categories[clean_cat] = []

                                    lbs = labels.find_next_siblings()

                                    for lb in lbs:
                                        clean_label = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, lb.text.encode('utf-8'))
                                        #print "CLEANED :", clean_label
                                        categories[clean_cat].append(clean_label)
                                        #new_label= new_label+"_"+lb.text

                                    # for cat_label in categories[new_label]:
                                    #     print new_label.encode('utf-8'),":",cat_label.encode('utf-8')

                            print "categories:",categories


              
                        # JSON write ALL to json folder
                      
                        json.dump({ 'id': html_file_number.encode('utf-8'), 'author': poem_author.encode('utf-8').lstrip(), 'title' : poem_title.encode('utf-8'), 'poet_DOB' : poet_DOB, 'poem_dop' : poem_dop.encode('utf-8'), 'labels':categories, 'poem' : poem.text.encode('utf-8') }, f_json)
                      
                        # 
                        # PANDAS
                        #




                        # OBSOLETE... but do it anyway... 
                        # WRITE Poems to txt folder
                        txt_fn = html_file_number+".txt"
                        #print "TXT Filename: ", txt_fn.encode('utf-8')

                        dir = DIR+'txt'
                        txt_fn_path = dir+"/"+txt_fn
                        # print "TXT Path/Filename: ",txt_fn_path.encode('utf-8')
                        f=open(txt_fn_path,'w+')

                        # REMOVED f.write(poem.text.encode('utf-8').strip())
                        
                        clean_poem = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, poem.text.encode('utf-8'))
                        
                        dp = clean_poem
                        #print dp

                        f.write(dp)

                        f.close();

            
f_json.close();    

print html_cnt,"html files processed"
print txt_cnt,"poems sent to txt files"
print "json file created at:",json_fn_path

