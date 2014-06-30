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
from collections import Counter

import nltk, re, pprint
from nltk import Text
from nltk.corpus import cmudict
from nltk.tokenize import WhitespaceTokenizer

############

type_of_run="ALL"
DATA_DIR  =  "../../../../data/poetryFoundation/"
# "...._69.txt" contains only 69 files for testing
JSON_FILE  =  "json/poetryFoundation_JSON_"+type_of_run+".txt"
csv_fn="output_"+type_of_run+".csv"
csv_PATH = DATA_DIR+csv_fn

############


from json import JSONDecoder
from functools import partial
from string import whitespace

import csv
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


#
# utilities
#

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
    '\xe2\x80\x94': '--',    # em dash
    '\xe2\x80\x93': '\''    # apostrophe

}


# USAGE new_str = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, text)
def replace_chars(match):
    char = match.group(0)
    return chars[char]


#count words (not tokens, and not punctuation)
nonPunct = re.compile('.*[A-Za-z0-9].*')  # must contain a letter or digit
def countWords(str):
    text = ['this', 'is', 'a', 'sentence', '.']
    filtered = [w for w in str if nonPunct.match(w)]
    counts = Counter(filtered)
    return len(counts)


# STRIP PUNCTUATION BUT KEEP IT TO BE ADDED LATER
def strip_punctuation_stressed(word):
    # define punctuations
    punctuations = '!()-[]{};:"\,<>./?@#$%^&*_~'
    my_str = word

    # remove punctuations from the string
    no_punct = ""
    punct=""
    for char in my_str:
        if char not in punctuations:
            ##print "CHAR:", char
            no_punct = no_punct + char
        else:
            punct = punct+char

    ##print "word:",no_punct,"punct:", punct
    return {'word':no_punct,'punct':punct}



# convert the cmudict prondict into just numbers
def strip_letters(ls):
    #print "strip_letters"
    nm = ''
    for ws in ls:
        #print "ws",ws
        for ch in list(ws):
            #print "ch",ch
            if ch.isdigit():
                nm=nm+ch
                #print "ad to nm",nm, type(nm)
    return nm



# clean up date of birth diverse formatting
def process_dob(poet_dob):

    birth = '0000'
    death = '0000'

    # empty
    if poet_dob == '':
        birth = '0000'
        death = '0000'

    # form "b. 1964"
    if poet_dob.split(".")[0]=='b' or poet_dob.split(".")[0]=='b.':
        birth=poet_dob.split(".")[1]
        death ='0000'

    # form "1964-2022"
    elif len(poet_dob.split("-"))>1:
        birth=poet_dob.split("-")[0]
        death =poet_dob.split("-")[1]

    return birth,death



def json_parse(fileobj, decoder=JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
         chunk.strip()
         buffer += chunk
         while buffer:
             try:
                 result, index = decoder.raw_decode(buffer)
                 yield result
                 buffer = buffer[index:]
             except ValueError:
                 # Not enough data to decode, read more
                 break



#
#  dict for csv file that pandas will read
#

master_list =[]
master_list.append(["id","author",'title','date_of_birth','date_of_death','date_of_publication','num_of_words','num_of_lines','num_of_verses','avg_word_len','avg_line_len','avg_lines_per_verse','longest_line','words_per_line','largest_word','poem','poem_stress_list','poem_stress_list_no_punct'])

#
# Load JSON
#

with open(DATA_DIR+JSON_FILE, 'r') as infh:
    
    cnt=0 
    no_lines=0

    largest_word_corpus_ls=[]
    prondict = cmudict.dict()
    
    
    # for every poem-file-object
    for data in json_parse(infh):
        # process object 
        cnt=cnt+1
        #print "cnt:", cnt
        labels_ls=[]
        # get the data out of json
        for idx, val in enumerate(data):

            #print idx, val
            #print data[val.encode('utf-8')].encode('utf-8')


            if val =='author':
                author = data[val.encode('utf-8')].encode('utf-8')
            elif val == 'title':
                title = data[val.encode('utf-8')].encode('utf-8')
            elif val == 'poet_DOB':
                poet_dob = data[val.encode('utf-8')].encode('utf-8')        
            elif val == 'poem_dop':
                date_of_publication = data[val.encode('utf-8')].encode('utf-8')
            elif val=='id':
                id=data[val.encode('utf-8')].encode('utf-8')
            elif val=='labels':
                categories =data[val.encode('utf-8')]
                #print "categories:",categories
                for k,l in categories.iteritems():
                    cat_no_cruft = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, k)
                    for lid,lv in enumerate(l):
                        labels_ls.append(cat_no_cruft+"_"+lv.encode('utf-8'))
                    
        
        # make dob normal
        date_of_birth, date_of_death = process_dob(poet_dob)
        #print (date_of_publication == "0000"), date_of_publication,date_of_birth,date_of_death 

        # DIRTY DATA! ~ clean str.isdigit() types out of this column in step 1
        # now in 2 make date of publication 20 years after birth if there is a birth date
        if date_of_publication == '0000':
            if date_of_birth.isdigit():
                if int(date_of_birth)>0:
                    date_of_publication = int(date_of_birth)+25
                    print "CHANGE date_of_publication:",date_of_publication
                    
            

        #
        # LOAD THE POEM
        #

        pf = open(DATA_DIR+"txt/"+id+".txt", 'rU')

        i=0
        v=0
        vb=0
        tvl=0
        num_empty_lines=0
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
        num_of_lines = 0
        num_of_verses = 0

        verse_lines_list=[]
        words_per_line=[]

        poem=""

        poem_stress_list=[]
        poem_stress_list_no_punct=[]

        for line in pf:

            i=i+1
            stress=''
            stress_no_punct=''
            
            poem=poem+line
            for word in nltk.word_tokenize(line.strip(' \t\n\r')):
                
                # get ride of unicode utf-8 cruft
                word_no_space = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, word)
                word_no_space = word_no_space.strip(' \t\n\r')
                # TOO MUCH gets rid of all hyphens, apostrophes etc..::: ''.join(e for e in word_no_space if e.isalnum())
                # residual space destruction

                word_len=word_len+len(word_no_space)
                #print len(word_no_space), word_no_space

                if len(word_no_space)>len(largest_word):
                    #print word_len,len(largest_word)
                    largest_word=word_no_space#.decode('utf-8')



            # 
            # FIND METRE (begin stress mess)
            # 

            for word in WhitespaceTokenizer().tokenize(line.strip(' \t\n\r')):    


                word_punct = strip_punctuation_stressed(word.lower())
                word = word_punct['word']
                punct = word_punct['punct']

                if word not in prondict:
                    #print "NOT in prondict:",word
                    stress= stress+"*"+word+"*"
                else:
                    #print word,stress,prondict[word][0]
                    stress = stress+strip_letters(prondict[word][0])
                    stress_no_punct=stress_no_punct+strip_letters(prondict[word][0])

                if len(punct)>0:
                    stress= stress+"*"+punct+"*"

            poem_stress_list.append(stress)
            poem_stress_list_no_punct.append(stress_no_punct)

            #print len(line),"~"+stress+"~",stress_no_punct,line


            #
            #   end of stress
            #



            line_len = len(nltk.word_tokenize(line))
            words_per_line.append(countWords(line.split()))
            #print "countWords(str):",countWords(line.split()),"line_len .. len(nltk.word_tokenize(line)):",line_len#,line
            num_of_words = num_of_words + line_len
            if line_len>longest_line:
                longest_line=line_len
            

            # find verse
            if len(nltk.word_tokenize(line))==0:
                vb=vb+1
                #print "~~~~~~~~~~~~~~~~~~~~~~~~~vb=",vb,i,"num_of_verses:",num_of_verses, "prev_verse_i:",prev_verse_i
                num_empty_lines=num_empty_lines+1
                if  (i-prev_verse_i-vb) > 0 :      
                    verse_len=i-prev_verse_i-vb
                    prev_verse_i=i
                    verse_lines_list.append(verse_len)
                    num_of_verses=num_of_verses+1
                    vb=0
                    tvl=tvl + verse_len

                    # #SPECIAL CASE: TITLE before a verse
                    # print "verse_len:",verse_len,"len(nltk.word_tokenize(line))",len(nltk.word_tokenize(line))

                    # if verse_len==1 and len(nltk.word_tokenize(line))==1:# and num_of_verses>=1:
                    #   print "TITLE before verse:",len(nltk.word_tokenize(line))
                    #   num_of_verses=num_of_verses-1
                    #   del verse_lines_list[-1]




        #print "~^^^^^special case... last verse does not have line after it: =",i,"prev_verse_i:",prev_verse_i
        if prev_verse_i<i:
            num_of_verses=num_of_verses+1
            verse_len=i-prev_verse_i-vb
            verse_lines_list.append(verse_len)
                
        # collate
                   
        if i!=0 and num_of_words>0: 
            
            num_of_lines = i- num_empty_lines
            avg_word_len = word_len/num_of_words
            avg_line_len = num_of_words / num_of_lines
            largest_word_corpus_ls.append(largest_word)
            
            # only one verse?
            if tvl==0:
                avg_lines_per_verse=i   
            else:
                avg_lines_per_verse = tvl/num_of_verses
        
            #        
            # BASIC FEATURES
            #

            print "id: ",id
            # print 'author:',author
            # print 'title:',title
            # print 'date_of_birth:', date_of_birth
            # print 'date_of_death:', date_of_death
            # print 'date_of_publication:',date_of_publication
            
            # print "num_of_words =",num_of_words
            # print "num_of_lines =",num_of_lines
            # print "num_of_verses =",num_of_verses

            # print "avg_word_len =",avg_word_len
            # print "avg_line_len =",avg_line_len
            
            # vl = ",".join(map(str,verse_lines_list))
            # print "verse_lines_list :", vl
            # print "avg_lines_per_verse=",avg_lines_per_verse
            
            # print "longest_line =", longest_line
           
            # print "largest_word_corpus_ls =", largest_word_corpus_ls
            # print "labels_ls =", labels_ls
            # print "words_per_line =", words_per_line
            # print "largest_word =", largest_word

            #
            # PANDAS DATA FRAME
            # 

            master_list.append([id,author,title,date_of_birth,date_of_death,date_of_publication,num_of_words,num_of_lines,num_of_verses,avg_word_len,avg_line_len,avg_lines_per_verse,longest_line,words_per_line,largest_word,poem,poem_stress_list,poem_stress_list_no_punct])

            # since labels might have been added
            if len(master_list[0])>len(master_list[-1]):
                for x in xrange(len(master_list[-1]),len(master_list[0])):
                    #print x
                    master_list[-1].append(0)
            #master_list[-1][len(master_list[-1]):len(master_list[0])]='ahah'


            #print "check to see if we need to add new column"

            for l in labels_ls:
                insert_needed  = True
                #print "loop through all lables"
                for m in master_list[0]:
                    #print "see if label exists"
                    l.rstrip(',')
                    l.rstrip(' ')
                    l.lstrip(' ')
                    if l == m:
                        #print "FOUND label in list already", l.encode('utf-8')
                        # put a 1 in since it has this label....
                        #master_list[-1].append(1)# [master_list[0].index(m)]=1
                        # print "master_list[0].index(l)",master_list[0].index(l)
                        # #print "master_list[0]",master_list[0]
                        # print "master_list[-1]",master_list[-1]
                        # print "len(master_list[-1]):",len(master_list[-1])
                        if len(master_list[-1])<master_list[0].index(l)+1:
                            master_list[-1].append(1)
                        else:
                            master_list[-1][master_list[0].index(l)]=1
                        # print "master_list[-1]",master_list[-1]
                        insert_needed = False
                        break
                if insert_needed:
                    #print "Inserting NEW label: ", l.encode('utf-8')
                    master_list[0].append(l.encode('utf-8'))

                    #print "Inserting zeroes for each row of new label"
                    for row in master_list:

                        if master_list.index(row) >0:
                            row.append(0)
                        #print len(row)
                    
                    master_list[-1][-1]=1
                    

            # BINARIZE & PUT in labels

        else:
            print "NO lines detected."
            no_lines=no_lines+1



# print '##########'
# print 'master_list'
# print '##########'

# for index, item in enumerate(master_list):
#         print index, item


pf.close()

with open(csv_PATH, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(master_list)

#
# test panda input 
#

print cnt,"poems processed"
print no_lines,"poems with no lines"
print "CSV file created at:",csv_PATH

df = pd.read_csv(csv_PATH)
print "DATAFRAME.head():\n",df.head(),"\n"
    


'''

10561 poems processed
9 poems with no lines
CSV file created at: ../../../../data/poetryFoundation/output.csv
/Users/jhave/anaconda/lib/python2.7/site-packages/pandas/io/parsers.py:1130: DtypeWarning: Columns (5) have mixed types. Specify dtype option on import or set low_memory=False.
  data = self._reader.read(nrows)
DATAFRAME.head():
      id              author                                     title  \
0     10      Averill  Curdy                                 Probation   
1  11053    Margaret  Walker                             For My People   
2  11099  Janet Loxley Lewis                          Carmel Highlands   
3  11288       Mary  Barnard  Remarks on Poetry and the Physical World   
4  11312       Dylan  Thomas   When All My Five and Country Senses See   

   date_of_birth  date_of_death date_of_publication  num_of_words  \
0              0              0                2005           188   
1           1915           1998                1937           527   
2           1899           1998                1938           110   
3           1909           2001                1938           108   
4           1914           1953                1938           127   

   num_of_lines  num_of_verses  avg_word_len      ...       \
0            35              7      3.968085      ...        
1            57             10      4.548387      ...        
2            14              2      4.572727      ...        
3            15              3      4.175926      ...        
4            14              2      4.031496      ...        

   Poetic Terms_Pantoum  Poetic Terms_Pantoum,   Region_Mexico  \
0                     0                       0              0   
1                     0                       0              0   
2                     0                       0              0   
3                     0                       0              0   
4                     0                       0              0   

  Poetic Terms_Quatrain Poetic Terms_Quatrain,  Poetic Terms_Aubade,   \
0                     0                       0                     0   
1                     0                       0                     0   
2                     0                       0                     0   
3                     0                       0                     0   
4                     0                       0                     0   

   Poetic Terms_Tercet  Poetic Terms_Ghazal,   Poetic Terms_Nursery Rhymes,   \
0                    0                      0                              0   
1                    0                      0                              0   
2                    0                      0                              0   
3                    0                      0                              0   
4                    0                      0                              0   

   Region_Russia  
0              0  
1              0  
2              0  
3              0  
4              0  

[5 rows x 278 columns] 

[Finished in 495.0s]
'''

