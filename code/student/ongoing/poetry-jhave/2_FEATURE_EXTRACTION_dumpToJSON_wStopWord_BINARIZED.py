#!/usr/bin/env python

"""

USING the JSON file

1.
load the JSON into pandas
http://pandas.pydata.org/pandas-docs/dev/generated/pandas.io.json.read_json.html
(valdiate: http://jsonlint.com/)

2.

convert the category and labels to numeric values


3. 
save as csv


4.
put into pandas df 

5.  NEXT FILE>>>>>>>>
classify?

6. TODO
groupby, plot, etc...
save the pandas with new columns
in clusters like 18th century etc...
create graphics of changing usage over time

keywords / concepts / line_lengths 
authors who are anomalies
develop vocaublaries for specific authors


"""



from __future__ import division
# from collections import Counter
from pprint import pprint

import nltk, re
from nltk import Text
from nltk.corpus import cmudict
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords

import os
import json

# ORDERED DICTIONARY orderedDict = collections.OrderedDict()
import collections

##### CHANGE THIS TO "6" OR "60" FOR TESTING or "ALL" for full corpus #########

type_of_run="ALL"

######################################################

DATA_DIR  =  "../../../../data/poetryFoundation/"
# "...._69.txt" contains only 69 files for testing

READ_JSON_FILE  =  "json/poetryFoundation_JSON_"+type_of_run+".txt"
csv_fn="output_"+type_of_run+".csv"
csv_PATH = DATA_DIR+csv_fn

# replace the csv with json with features numerized
WRITE_JSON_PATH = DATA_DIR+"json/STEP2_poetryFoundation_JSON_"+type_of_run+".txt"


try:
    if os.path.isfile(WRITE_JSON_PATH):
            os.unlink(WRITE_JSON_PATH)
except Exception, e:
        print e


# JSON file
f_json=open(WRITE_JSON_PATH,'a')

############

import csv
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


#
# utilities
#
import import_utilities


#
#  dict for csv file that pandas will read
#

master_list =[]
# FULL NO POEM  
#master_list.append(["id","author",'title','date_of_birth','date_of_death','date_of_publication','num_of_words','num_of_non_empty_lines','num_of_verses','avg_word_len','avg_line_len','avg_lines_per_verse','longest_line','words_per_line','largest_word','poem_stress_list','poem_stress_list_no_punct','chars_per_line'])

# FULL NO POEM  & no  poem_stress_list_no_punct
master_list.append(["id","author",'title','date_of_birth','date_of_death','date_of_publication','num_of_words','num_of_non_empty_lines','num_of_verses','avg_word_len','avg_line_len','avg_lines_per_verse','longest_line','words_per_line','largest_word','chars_per_line'])

# PARTIAL master_list.append(["id","author",'title','date_of_birth','date_of_death','date_of_publication','num_of_words','num_of_non_empty_lines','num_of_verses','avg_word_len','avg_line_len','avg_lines_per_verse','longest_line','words_per_line','largest_word','poem_stress_list','poem_stress_list_no_punct','chars_per_line'])

# ADD stopwords (to measure the occurence of stopwords, an effective author identification tool)

#print len(import_utilities.stopwords_ls),"BEFORE len (master_list) = ", len(master_list[0])
for s in import_utilities.stopwords_ls:
    master_list[0].append(s)

#print "AFTER len (master_list) = ", len(master_list[0])

#
# Load JSON
#

with open(DATA_DIR+READ_JSON_FILE, 'r') as infh:
    
    cnt=0 
    no_lines=0

    largest_word_corpus_ls=[]
    prondict = cmudict.dict()
    
    
    # for every poem-file-object
    for data in import_utilities.json_parse(infh):
        # process object 
        cnt=cnt+1
        #print "cnt:", cnt
        labels_ls=[]

        author='UNKNOWN'
        title='UNKNOWN'

        # get the data out of json
        for idx, val in enumerate(data):

            #print idx, val
            #print data[val.encode('utf-8')].encode('utf-8')



            if val =='author':
                author = data[val.encode('utf-8')].encode('utf-8')
                #`print author
            elif val == 'title':
                title = data[val.encode('utf-8')].encode('utf-8')
            elif val == 'poet_DOB':
                poet_dob = data[val.encode('utf-8')].encode('utf-8')        
            elif val == 'poem_dop':
                date_of_publication = data[val.encode('utf-8')].encode('utf-8')
            elif val=='id':
                id=data[val.encode('utf-8')].encode('utf-8')
            elif val=='poem':
                poem_from_csv=data[val.encode('utf-8')].encode('utf-8')
            elif val=='labels':
                categories =data[val.encode('utf-8')]
                #print "categories:",categories
                for k,l in categories.iteritems():
                    cat_no_cruft = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, k)
                    if cat_no_cruft != 'Poet':
                        for lid,lv in enumerate(l):
                            lv_no_cruft = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, lv)
                            labels_ls.append(cat_no_cruft+"_"+lv_no_cruft)#.encode('utf-8'))
                        
            
        # make dob normal
        date_of_birth, date_of_death = import_utilities.process_dob(poet_dob)
        #print (date_of_publication == "0000"), date_of_publication,date_of_birth,date_of_death 

        # DIRTY DATA! ~ clean str.isdigit() types out of this column in step 1
        # now in 2 make date of publication 20 years after birth if there is a birth date
        if date_of_publication == '0000':
            if date_of_birth.isdigit():
                if int(date_of_birth)>0:
                    date_of_publication = int(date_of_birth)+25
                    #print "CHANGE date_of_publication:",date_of_publication
                    
            

        #
        # LOAD THE POEM
        #

        pf = open(DATA_DIR+"txt/"+id+".txt", 'rU')

        i=0
        v=0
        vb=0
        tvl=0
        num_empty_lines=0.
        prev_verse_i=0 
        line_len = 0

        largest_word=""
       
        longest_line=0
        shortest_line=0

        avg_line_len = 0
        avg_words_per_line = 0

        avg_word_len = 0 
        word_len = 0
        avg_lines_per_verse=0
        
        num_of_words = 0
        num_of_non_empty_lines = 0
        num_of_verses = 0

        verse_lines_list=[]
        words_per_line=[]
        chars_per_line=[]

        poem=""

        poem_stress_list=[]
        poem_stress_list_no_punct=[]

        stops_dict = {}#collections.OrderedDict()
        sc=0
        for s in import_utilities.stopwords_ls:
            stops_dict[s]=0
            sc+=1
            #print sc,"init",s,stops_dict[s]
        #print len(import_utilities.stopwords_ls),"len(stops_dict)",len(stops_dict)

        for line in pf:

            #print i,len(line.strip(' \t\n\r')),"'"+line+"'"          
            if i==0 and len(line.strip(' \t\n\r'))==0:
                #print "EMPTY FIRST LINE"
                pass
            else:
                i=i+1 
                stress=''
                stress_no_punct=''
                
                poem=poem+line
                for word in nltk.word_tokenize(line.strip(' \t\n\r')):
                    
                    # get ride of unicode utf-8 cruft
                    word_no_space = re.sub('(' + '|'.join(import_utilities.chars.keys()) + ')', import_utilities.replace_chars, word)
                    word_no_space = word_no_space.strip(' \t\n\r')
                    # TOO MUCH gets rid of all hyphens, apostrophes etc..::: ''.join(e for e in word_no_space if e.isalnum())
                    # residual space destruction

                    
                    # print "len:",len(word_no_space), "word_no_space:", word_no_space
                    # print "countWords("+word_no_space+"):",countWords(word_no_space)

                    #########################
                    # stopword usage        #
                    #########################
                    if word.lower() in import_utilities.stopwords_ls:
                        stops_dict[word.lower()] += 1 
                        #print word.lower(),stops_dict[word.lower()] 

                    #################################################################
                    # CHECK to see if line is simply _______ or ******* or $##$$$$  #
                    #################################################################
                    if import_utilities.countWords(word_no_space)==0 and len(word_no_space)>0:
                        #print "this word is probably just underscores or asterixes do NOT include it in avg_word_length"
                        pass
                    else:
                        word_len=word_len+len(word_no_space)


                    if len(word_no_space)>len(largest_word):
                        #print word_len,len(largest_word)
                        largest_word=word_no_space#.decode('utf-8')



                #####################################
                # FIND METRE (begin stress mess)    #
                #####################################

                for word in WhitespaceTokenizer().tokenize(line.strip(' \t\n\r')):    


                    word_punct = import_utilities.strip_punctuation_stressed(word.lower())
                    word = word_punct['word']
                    punct = word_punct['punct']

                    if word not in prondict:
                        #print "NOT in prondict:",word
                        stress= stress+"*"+word+"*"
                    else:
                        #print word,stress,prondict[word][0]
                        stress = stress + import_utilities.strip_letters(prondict[word][0])
                        stress_no_punct=stress_no_punct + import_utilities.strip_letters(prondict[word][0])

                    if len(punct)>0:
                        stress= stress+"*"+punct+"*"

                poem_stress_list.append(stress)
                poem_stress_list_no_punct.append(stress_no_punct)

                #print len(line),"~"+stress+"~",stress_no_punct,line


                #
                #   end of stress
                #


                # find line length
                if import_utilities.countChars(line.split())!=0:
                    line_len = len(nltk.word_tokenize(line))
                    words_per_line.append(import_utilities.countWords(line.split()))
                    chars_per_line.append(import_utilities.countChars(line.split()))
                    
                    #print i, chars_per_line, words_per_line, line
                    #print "words_per_line:",countWords(line.split())
                    #print "line_len .. len(nltk.word_tokenize(line)):",line_len
                    #print "line:",line
                    if line_len<0:
                        line_len=0
                    num_of_words = num_of_words + line_len
                    if line_len>longest_line:
                        longest_line=line_len
                else:
                    if i==1:
                        #print "FIRST line empty:",i,import_utilities.countChars(line.split())
                        i-=1
                        num_empty_lines-=1
                
                    

                # find verse
                if len(nltk.word_tokenize(line))==0:
                    vb=vb+1
                    #print "~~~~~~~~~~~~~~~~~~~~~~~~~vb=",vb,"\ni=",i,"  num_of_verses:",num_of_verses, "   prev_verse_i:",prev_verse_i
                    num_empty_lines=num_empty_lines+1
                    if  (i-prev_verse_i-vb) > 0 :      
                        verse_len=i-prev_verse_i-vb
                        prev_verse_i=i
                        verse_lines_list.append(verse_len)
                        num_of_verses=num_of_verses+1
                        vb=0
                        tvl=tvl + verse_len

                        # #SPECIAL CASE: TITLE or diacritic before a verse
                        #print "verse_len:",verse_len,"countWords(line_previous)",countWords(line_previous), "line_previous:",line_previous

                        if verse_len==1 and import_utilities.countWords(line_previous)==0:# and num_of_verses>=1:
                            
                            num_of_verses=num_of_verses-1
                            #print "TITLE before verse or decorative # ~ . : detect from num_of_verses:",num_of_verses
                            del verse_lines_list[-1]


                line_previous=line




        #print "~^^^^^special case... last verse does not have line after it: =",i,"prev_verse_i:",prev_verse_i
        if prev_verse_i<i:
            num_of_verses=num_of_verses+1
            verse_len=i-prev_verse_i-vb
            verse_lines_list.append(verse_len)
                
        # collate
                   
        if i!=0 and num_of_words>0: 
            
            num_of_non_empty_lines = i- num_empty_lines

            #print "i=",i,"num_empty_lines:",num_empty_lines, "num_of_non_empty_lines =",num_of_non_empty_lines


            avg_word_len = word_len/num_of_words
            avg_line_len = num_of_words / num_of_non_empty_lines
            largest_word_corpus_ls.append(largest_word)
            
            # only one verse?
            if num_of_verses==1:
                avg_lines_per_verse=i   
            else:
                avg_lines_per_verse = num_of_non_empty_lines/num_of_verses
        




            #        
            # BASIC FEATURES
            #

            print "\nid: ",id,cnt
            print 'author:',author
            print 'title:',title
            # print 'date_of_birth:', date_of_birth
            # print 'date_of_death:', date_of_death
            # print 'date_of_publication:',date_of_publication
            
            # print "num_of_words =",num_of_words
            # print "num_empty_lines =",num_empty_lines
            # print "num_of_verses =",num_of_verses

            # print "word_len:",word_len

            # print "avg_word_len =",avg_word_len
            # print "avg_line_len =",avg_line_len
            
            # vl = ",".join(map(str,verse_lines_list))
            # print "verse_lines_list :", vl
            # print "avg_lines_per_verse =",avg_lines_per_verse
            
            # print "longest_line =", longest_line
           
            # print "largest_word_corpus_ls =", largest_word_corpus_ls
            # print "labels_ls =", labels_ls

            # print "words_per_line =", words_per_line
            # print "chars_per_line =", chars_per_line
            # print "largest_word =", largest_word
            # print "largest_word length=" , len(largest_word)

            # print "poem_stress_list: ", poem_stress_list
            #print "poem_stress_list_no_punct: ", poem_stress_list_no_punct



            #
            # PANDAS DATA FRAME
            # 

            #


            # FULL NO POEM   
            #master_list.append([id,author,title,date_of_birth,date_of_death,date_of_publication,num_of_words,num_of_non_empty_lines,num_of_verses,avg_word_len,avg_line_len,avg_lines_per_verse,longest_line,words_per_line,largest_word,poem_stress_list,poem_stress_list_no_punct,chars_per_line])

            # FULL NO POEM  & no  poem_stress_list_no_punct

            if "Barnard" not in author and "175184" != id:
                master_list.append([id,author,title,date_of_birth,date_of_death,date_of_publication,num_of_words,num_of_non_empty_lines,num_of_verses,avg_word_len,avg_line_len,avg_lines_per_verse,longest_line,words_per_line,largest_word,chars_per_line])

            #master_list.append([id,author,title,date_of_birth,date_of_death,date_of_publication,num_of_words,num_of_non_empty_lines,num_of_verses,avg_word_len,avg_line_len,avg_lines_per_verse,longest_line,words_per_line,largest_word,poem_stress_list,poem_stress_list_no_punct,chars_per_line])

            ####################
            # APPEND Stop words
            ####################
            
                sorted_sd =collections.OrderedDict(sorted(stops_dict.items()))
                for s in sorted_sd:
                    master_list[-1].append(sorted_sd[s.encode('utf-8')])
                #print "APPEND",s,sorted_sd[s],len(master_list[-1])

            # # since labels might have been added
            # if len(master_list[0])>len(master_list[-1]):
            #     for x in xrange(len(master_list[-1]),len(master_list[0])):
            #         #print x
            #         master_list[-1].append(0)
            # #master_list[-1][len(master_list[-1]):len(master_list[0])]='ahah'


            # #print "check to see if we need to add new column"

            # for l in labels_ls:
            #     insert_needed  = True
            #     #print "loop through all lables"
            #     for m in master_list[0]:
            #         #print "see if label exists"
            #         l.rstrip(',')
            #         l.rstrip(' ')
            #         l.lstrip(' ')
            #         if l == m:
            #             #print "FOUND label in list already", l.encode('utf-8')
            #             # put a 1 in since it has this label....
            #             #master_list[-1].append(1)# [master_list[0].index(m)]=1
            #             # print "master_list[0].index(l)",master_list[0].index(l)
            #             # #print "master_list[0]",master_list[0]
            #             # print "master_list[-1]",master_list[-1]
            #             # print "len(master_list[-1]):",len(master_list[-1])
            #             if len(master_list[-1])<master_list[0].index(l)+1:
            #                 master_list[-1].append(1)
            #             else:
            #                 master_list[-1][master_list[0].index(l)]=1
            #             # print "master_list[-1]",master_list[-1]
            #             insert_needed = False
            #             break
            #     if insert_needed:
            #         new_lbl= l.replace (" ", "_").lower().encode('utf-8')
            #         #print "Inserting NEW label: ", new_lbl
            #         master_list[0].append(new_lbl)

            #         #print "Inserting zeroes for each row of new label"
            #         for row in master_list:

            #             if master_list.index(row) >0:
            #                 row.append(0)
            #             #print len(row)
                    
            #         master_list[-1][-1]=1
                    


        else:
            print "NO lines detected."
            no_lines=no_lines+1



# print '##########'
# print 'master_list'
# print '##########'

# for index, item in enumerate(master_list):
#          print index, item


pf.close()



#
# (holy fuckin shit did this simple traverse ever take me forever: 1 day approx.)
# PUT NUMERIC VALUES INTO THEIR OWN COLUMNS in a dictionary with keys so it can be written as JSON then imported to pandas
# #
jcnt=0
master_list_of_dictionaries=[]
for ml in master_list:
    tmp_dict={}
    tmp_list=[]
    print len(ml),master_list.index(ml)
    if master_list.index(ml)!=0:
        for k,v in enumerate(ml):
            key =master_list[0][k]
            #if key != v:
            #print k,key,v
            tmp_dict[key.replace("'", '"')]= v
            if "words_per_line" in key:
                for i,wpl in enumerate(v):
                    tmp_dict["words_per_line_"+str(i).encode('utf-8')]=float(wpl)
            elif "chars_per_line" in key:
                for i,wpl in enumerate(v):
                    tmp_dict["chars_avg_per_line_"+str(i).encode('utf-8')]=float(wpl)
            elif "poem_stress_list_no_punct" in key:
                for i,wpl in enumerate(v):
                    #print "'"+wpl+"'",wpl.rstrip().lstrip().isdigit()
                    if len(wpl)==0:
                        print "zero"
                        wpl=0
                    tmp_dict["stress__on_line_"+str(i).encode('utf-8')]=float(wpl)
            elif "largest_word" in key:
                tmp_dict["largest_word_length"]=len(key)
    
    ##################
    # pre-STORAGE JSON  #
    ##################

    tmp_list.append(tmp_dict)
    master_list_of_dictionaries.append(tmp_dict)
    # try:
    #     json.dump(tmp_dict, f_json)
    #     jcnt+=1
    #     master_list_of_dictionaries.append(tmp_dict)
    # except UnicodeDecodeError:
    #     print "UnicodeDecodeError",id,author,title
    #     error_str+=id+" ~ "
    #     print len(master_list), master_list.index(ml)
    #     continue

    # CANNOT because json load needs dict wrapped in list
    # error_str=""
    # try:
    #     json.dump(tmp_dict, f_json)
    #     jcnt+=1
    # except UnicodeDecodeError:
    #     print "UnicodeDecodeError",id,author,title
    #     error_str+=id+" ~ "
    #     print len(master_list), master_list.index(ml)
    #     continue

        #json.dump(',',f_json)
        

################# 
#  write csv    #
#################

# with open(csv_PATH, "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(master_list)
                   
# print "\npprint:"
#pprint(master_list_of_dictionaries)

#############################
#  DUMP TO json             #
#############################   
error_str=""
# 
# try:
#     json.dump(master_list_of_dictionaries, f_json)
# except UnicodeDecodeError:
#     print "UnicodeDecodeError",id,author,title
#     error_str+=id+" ~ "
#     pass

json.dump(master_list_of_dictionaries, f_json)    
f_json.close(); 

print error_str
#
# test panda input 
#

print cnt,"poems processed"
print no_lines,"poems with no lines"
print jcnt,"poems in json",WRITE_JSON_PATH
#print "binarized CSV file created at:",csv_PATH

# df = pd.read_csv(csv_PATH)
# print "\nDATAFRAME.head():\n",df.head(),"\n"
# print "\nDATAFRAME.tail():\n",df.tail(),"\n"    
