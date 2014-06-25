#!/usr/bin/env python

"""

USING the JSON file
with NLTK tokenizer
to see if space stripping solved:
FAIL 



1.
retrieve the name of associated txt file 
containing the poem

2.
open the txt file

3. 
collect features
-- concentrating on features that are not usually bothered with in prose:
line length, spacing, layout, verse length, etc....


###################
HELP! Big bug: space exists, refuses to leave....
    before it goes it must be counted....
    but right now it is creating an error in the word counted
####################


####################
TODO:: 
    put features into pandas / numpy data structure
    apply some nltk extraction
    classify
    display


"""


from __future__ import division

import nltk, re, pprint
from nltk import Text


DATA_DIR  =  "../../../../data/poetryFoundation/"
# "...._69.txt" contains only 69 files for testing
JSON_FILE  =  "json/poetryFoundation_JSON_6.txt"


from json import JSONDecoder
from functools import partial
from string import whitespace

#import nltk


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

with open(DATA_DIR+JSON_FILE, 'r') as infh:
    cnt=0 
    largest_word_ls=[]
    Author=''
    Title=''
    poet_DOB=''
    poem_dop=''
    
    for data in json_parse(infh):
        # process object 
        cnt=cnt+1
        print "cnt:", cnt
        for idx, val in enumerate(data):

            #print idx, val
            if idx==1:
                #print val['Author'].encode('utf-8')
                Author = val['Author'].encode('utf-8')
            elif idx==2:
                #print val['Title'].encode('utf-8')
                Title = val['Title'].encode('utf-8')
            elif idx==3:
                #print val['poet_DOB'].encode('utf-8')
                poet_DOB = val['poet_DOB'].encode('utf-8')              
            elif idx==4:
                #print val['poem_dop'].encode('utf-8')
                poem_dop = val['poem_dop'].encode('utf-8')                   

            # retrieve the name of associated txt file containing the poem
            if idx==0:
                txt_fn= DATA_DIR+"txt/"+val+".txt"
                

                # LOAD THE POEM HERE
                #
                # features
      

                pf = open(txt_fn, 'rU')

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

                for line in pf:

                    i=i+1
                    
                    for word in nltk.word_tokenize(line.strip(' \t\n\r')):
                        word_no_space =''.join(e for e in word if e.isalnum())
                        word_len=word_len+len(word_no_space)

                        print len(word_no_space), word_no_spacen

                        if len(word_no_space)>len(largest_word):
                            #print word_len,len(largest_word)
                            largest_word=word

                    line_len = len(nltk.word_tokenize(line))
                    #print"line_len:",line_len,line
                    num_of_words = num_of_words + line_len
                    if line_len>longest_line:
                        longest_line=line_len
                    

                    # find verse
                    if len(nltk.word_tokenize(line))==0:
                        vb=vb+1
                        num_empty_lines=num_empty_lines+1
                        if  (i-prev_verse_i-vb) > 1 :      
                            verse_len=i-prev_verse_i-vb
                            prev_verse_i=i
                            verse_lines_list.append(verse_len)
                            num_of_verses=num_of_verses+1
                            vb=0
                            tvl=tvl + verse_len
                            #print "verse"
                             
                    #

                # collate
                           
                if i!=0: 
                    
                    num_of_lines = i- num_empty_lines
                    avg_word_len = word_len/num_of_words
                    avg_line_len = num_of_words / num_of_lines
                    largest_word_ls.append(largest_word)
                    
                    # only one verse?
                    if tvl==0:
                        avg_lines_per_verse=i   
                    else:
                        avg_lines_per_verse = tvl/num_of_verses
                    
            # BASIC FEATURES
            print "filename: ",txt_fn
            print 'Author',Author
            print 'Title',Title
            print 'poet_DOB',poet_DOB
            print 'poem_dop',poem_dop
            
            print "num_of_words =",num_of_words
            print "num_of_lines =",num_of_lines
            print "num_of_verses =",num_of_verses

            print "avg_word_len =",avg_word_len
            print "avg_line_len =",avg_line_len
            
            vl = ",".join(map(str,verse_lines_list))
            print "verse_lines_list :", vl

            print "avg_lines_per_verse=",avg_lines_per_verse
            
            print "longest_line =", longest_line
            print "largest_word =", largest_word
            print "largest_word =", largest_word_ls
            
                #data_dict["filename"] = val

            pf.close()

    print '[%s]' % ', '.join(map(str, largest_word_ls ))
