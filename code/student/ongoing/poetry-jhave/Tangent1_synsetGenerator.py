#! /usr/bin/env python

"""

MOodified from
https://github.com/shanbady/NLTK-Boston-Python-Meetup

Tangent#1 : generate a poem use synsets from nltk wordnet to replace all but stopwords
Goal: generate a set of poems from entire corpus.

1. 
Read in a .txt file poem

2.
For each poem: 

    Tokenize
    Find synsets
    Select replacement word

3. 
Write new poem to txt file in "generated/tangent1_synset/"


"""


from __future__ import division

from random import randint
from random import shuffle

from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.corpus import cmudict,wordnet as wn
from nltk.corpus import stopwords
import nltk, re, pprint
from nltk import Text

import re
import os
import sys
import random



#
#  IMPORTANT : while testing change this dir
#
DATA_DIR  =  "../../../../data/poetryFoundation/txt/"
#  NOTE: "txt_6" directory contains only 6 files for testing
GENERATED_DIR  =  "../../../../data/poetryFoundation/generated/tangent1_synset/txt"




#
# HELPR FUNCTION: FIND A SIMILAR WORD OF SIMILAR SIZE
#

def find_synset_word(word):
    

    wordstring=word

    # get rid of punctuation
    #wordstring.translate(None, string.punctuation)
    word_punct = strip_punctuation(word)
    word = word_punct['word']
    punct = word_punct['punct']

    syllableSize=syllables_en.count(word)

    synsets = wn.synsets(word)
    shuffle(synsets)
    #print word,"synset:",synsets


    replacement_candidates = []

    for syns in synsets:

        lemmas =  syns.lemma_names
        #print "LEMMAS:",lemmas
        #print "hypernyms:",syns.hypernyms()
        #print "hyponyms:",syns.hyponyms()
        #print "holonyms:",syns.member_holonyms()
        #print syns,"antonyms:",syns.lemmas[0].antonyms()
        
        for w in lemmas:
            replacement_candidates.append(w)

        for w in syns.hyponyms():
            replacement_candidates.append(w.name.split(".")[0])

        for w in syns.hypernyms():
            replacement_candidates.append(w.name.split(".")[0])

        for w in syns.member_holonyms():
            replacement_candidates.append(w.name.split(".")[0])

        #print "replacement_candidates:",replacement_candidates

        for wordstring in replacement_candidates:
            #find an approximate matchb
            #print "wordstring in name:",wordstring
            if (approx_equal(wordstring,word) and wordstring.lower() != word.lower() and len(wordstring)>len(word)):
                #print "SYNSET approx_equal:",word,wordstring
                return wordstring+punct
            #len same, word not
            if(len(wordstring) == len(word) and wordstring.lower() != word.lower()):
                #print "SYNSET len same, word not:",word,wordstring
                return wordstring+punct

            if(syllables_en.count(wordstring) == syllableSize and wordstring.lower() != word.lower()):
                #print "SYNSET syllable same, word not:",word,wordstring
                return wordstring+punct
     

    #print "SYNSET escape case, return original:",word
    return    wordstring





#
# HELPER FUNCTIONs
#

# TEST FOR APPROX. EQUIVALENCE
def approx_equal(self, other, delta=4):
    count = abs(len(self) - len(other))
    for c,k in zip(self, other):
        count += c != k
    return count <= delta

# STRIP PUNCTUATION BUT KEEP IT TO BE ADDED LATER
def strip_punctuation(word):
    # define punctuations
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    my_str = word

    # remove punctuations from the string
    no_punct = ""
    punct=""
    for char in my_str:
        if char not in punctuations:
            ##print "CHAR:", char
            no_punct = no_punct + char
        else:
            punct = char

    ##print "word:",no_punct,"punct:", punct
    return {'word':no_punct,'punct':punct}



personal_pronouns = ["i","me","we","us","you","she","her","he","him","it","they","them"]

#
#    READ FILES
#

for subdir, dirs, files in os.walk(DATA_DIR):
    for file in files:
        #print subdir+'/'+file
        html_file_number=file.split(".")[0]
        print "\n",html_file_number
        # 
        # & PARSE POEM
        #
        cnt=0
        new_poem = ""
       
        pf = open(subdir+file, 'rU')
        for line in pf:

            wordmap = []
            new_line=""

            if len(line)>0:
                new_line="\n"

            cnt=cnt+1
            #print len(line),"line is long"
            

            # if line is not empty, push each word of line into array with syllable cnt
            if len(line) > 1:

                
                for word in nltk.word_tokenize(line.strip(' \t\n\r')):

                    if not word.lower() in stopwords.words('english'):
                        similarterm = find_synset_word(word)
                        replacement_word = similarterm
                        ##print "original: *"+word+"* replacement:", replacement_word
                        new_line += replacement_word+" "
                    else:
                        if word.isalpha():
                            if not word.lower() in personal_pronouns :
                                #print "skip STOP word: *"+word+"*"
                                new_line += word+" "
                            else:
                                replacement_word = random.choice(personal_pronouns)
                                #print word+" random personal_pronouns: *"+replacement_word+"*"
                                new_line += replacement_word+" "
                        else:
                              #print "verse GAP"
                              new_line += "\n"
            #else:
                #print len(line),"line break"
                #new_line += "\n"



            

                
            new_poem += new_line

        #print "\nLINE:",line,"\nNEW LINE:",new_line



        # 
        # WRITE new POEM TO FILE
        #
        txt_fn = html_file_number+".txt"
        #print "TXT Filename: ", txt_fn.encode('utf-8')

        txt_fn_path = GENERATED_DIR+"/"+txt_fn
        #print "TXT Path/Filename: ",txt_fn_path.encode('utf-8')
        f=open(txt_fn_path,'w+')

        dp = new_poem
        f.write(dp)

        f.close();
        
    	#print new_poem





    

