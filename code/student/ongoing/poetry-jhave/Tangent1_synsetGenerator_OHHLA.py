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

WhitespaceTokenizer = nltk.WhitespaceTokenizer

import re
import os, datetime
import sys
import random
import string

#
# pattern.en
# module to singularize and do verb tenses
# http://www.clips.ua.ac.be/pattern
#
from pattern.en import pluralize, singularize
from pattern.en import comparative, superlative
from pattern.en import conjugate, lemma, lexeme, PARTICIPLE
# print conjugate('googled', tense=PARTICIPLE, parse=True)  
# >>> googling
# NOTE: it also does sentiment, returns a tuple...
# from pattern.en import sentiment
# and can be used with weights using http://sentiwordnet.isti.cnr.it/ 

#
#  IMPORTANT : while testing change this dir
#
DATA_DIR  =  "../../../../data/poetry/ohhla/ohhla_txt_files_1/"
#  NOTE: "txt_6" directory contains only 6 files for testing
GENERATED_DIR  =  "../../../../data/poetry/ohhla/ohhla_generated/synsetGenerator_"+datetime.datetime.now().strftime('%Y-%m-%d_%H')+"/"

# add meronymns
# introduce a swearing shuffle
# brands array
# spice it up: porn & poetry terms (define a balancing term for that)


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
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~_'''
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
            no_punct = no_punct+' '

    ##print "word:",no_punct,"punct:", punct
    return {'word':no_punct,'punct':punct}

#Check whether 'str' contains ANY punctuation
def containsAnyPunct(str):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~_'''
    return 1 in [c in str for c in punctuations]

def isAllPunct(s):
    return all(c in string.punctuation for c in s)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# replace digits with other digits...
def replaceNumbers(inputString):
    outputString =''
    for char in inputString:
        if char.isdigit():
            char = random.randrange(9)
            #print "DIGIT",char
        outputString +=str(char)
    return outputString

# STRIP PUNCTUATION BUT KEEP IT TO BE ADDED LATER
def strip_underscore(word):
    # define punctuations
    punctuations = '''_'''
    my_str = word

    # remove _ from the string
    no_punct = ""
    for char in my_str:
        if char not in punctuations:
            ##print "CHAR:", char
            no_punct = no_punct + char
        else:
            no_punct = no_punct+' '

    ##print "word:",no_punct,"punct:", punct
    return no_punct


labels_to_keep = ['Artist','Album','Song','Typed', 'VERSE','CHORUS']

personal_pronouns = ["i","me","we","us","you","she","her","he","him","it","they","them"]

#################################################
#                                               #
#    READ FILES                                 #
#                                               #
#################################################
for subdir, dirs, files in os.walk(DATA_DIR):
    for file in files:
        print subdir+file
        if ".txt" in file:
            html_file_number=file.split(".")[0]
            #print "file",file,"\nhtml_file_number",html_file_number
            # 
            # & PARSE POEM
            #
            cnt=0
            new_poem = ""
           
            pf = open(subdir+file, 'rU')
            for line in pf:


                '''

KEEP

<pre>
Artist: Spice 1
Album:  1990-Sick
Song:   1-800 (Str8 from the Pen)
Typed by : Timo.Scheffler@allgaeu.org

                '''

                
                if '<pre>' not in line and '</pre >' not in line and '< /pre >' not in line:

                    # POS part-of-speech
                    line_pos_tags = nltk.pos_tag(line.strip(' \t\n\r').split(' '))
                    # print "\n",line
                    # print line_pos_tags

                    wordmap = []
                    new_line=""

                    if len(line)>0:
                        new_line="\n"

                    cnt=cnt+1
                    #capitalize artist,album,song
                    label_idx=99
                    skip_line=False

                    # if line is not empty, push each word of line into array with syllable cnt
                    if len(line) > 1:

                        widx=0
                        # get each WORD
                        for word in line.strip(' \t\n\r').split(' '):

                            # scramble emails
                            if '@' in word:
                                word = ''.join(random.sample(word,len(word)))

                            # deal with end case
                            if '</pre>' in word:
                                word = word.split('</pre>')[0]

                            #####################################
                            # non-empty line, start replacement #
                            #####################################
                            if len(word)>0:

                                # print word,"widx:",widx," line_pos_tags[widx][0]:",line_pos_tags[widx][0]," line_pos_tags[widx][1]:",line_pos_tags[widx][1]
                                # booleans that allow us to leave the VERSE CHORUS format
                                labelling=False
                                VC = False
                                
                                # if it's ALL punctuation, don't change it
                                if isAllPunct(word):
                                    new_line += word+' '
                                # if it's numeric, shuffle it
                                elif hasNumbers(word):
                                    new_line += replaceNumbers(word)+' '
                                    #print new_line
                                else:
                                    # is it Artist, Album, Song
                                    for ltk in labels_to_keep:
                                        if ltk in word:
                                            #print 'found an ',ltk
                                            labelling = True
                                            label_idx=0

                                            if 'VERSE' in ltk or 'CHORUS' in ltk:
                                                #print "skip this line"
                                                new_line += ltk+" "
                                                skip_line=True
                                            else:
                                                replacement_word=ltk
                                                if 'Typed' not in ltk:
                                                    new_line += replacement_word+": "
                                                else:
                                                    new_line += replacement_word+" "



                                    #
                                    # REPLACEMENT of pronouns with compressed verb (as in I'd)
                                    #                
                                    if len(word.split("'"))>1:

                                        if word.split("'")[0] in personal_pronouns:
                                            replacement_word = random.choice(personal_pronouns)+"'"+word.split("'")[1]+' '
                                            #print "COMPOSITE pronoun'verb word:'"+word+"'    replacement:",replacement_word

                                        new_line += replacement_word

                                    elif not word.lower() in stopwords.words('english') and not labelling and not skip_line:


                                        similarterm = find_synset_word(word)

                                        # is it a TRUNCATED VERB slang as in singin or wishin
                                        if similarterm == word and len(word)>2 and 'in' in word[-2:]:
                                            similarterm = find_synset_word(word+'g')
                                            #print "TRUNCATED SLANG word: '"+word+"'",similarterm
                                            interim = lemma(similarterm)
                                            #print interim
                                            similarterm = conjugate(interim, tense=PARTICIPLE, parse=True)[:-1] 
                                            # print word,"widx:",widx," line_pos_tags[widx][0]:",line_pos_tags[widx][0]," line_pos_tags[widx][1]:",line_pos_tags[widx][1]
                                           

                                        # # is it a SWEAR WORD
                                        # if similarterm == word and word in curses:
                                        #     similarterm = random.choice(curse)
                                        #     print "SWEAR WORD word: '"+word+"'",similarterm

                                        replacement_word = strip_underscore(similarterm)
                                        replacement_word = replaceNumbers(replacement_word)

                                        if label_idx<2:
                                            replacement_word = ' '.join(word[0].upper() + word[1:] for word in replacement_word.split())
                                            #print "CAPITALIZE",replacement_word

                                        print "word: '"+word+"'' replacement: '"+replacement_word+"'"
                                        new_line += replacement_word+" "

                                    elif not labelling and not skip_line:
                                        if word.isalpha():
                                            if not word.lower() in personal_pronouns :
                                                #print "skip STOP word: *"+word+"*"
                                                new_line += word+" "
                                            else:
                                                replacement_word = random.choice(personal_pronouns)
                                                #print word+" random personal_pronouns: *"+replacement_word+"*"
                                                new_line += replacement_word+" "
                                        else:
                                              print "verse GAP"
                                              new_line += "\n"
                            #else:
                                #print len(line),"line break"
                                #new_line += "\n"

                                widx+=1



                    

                    #
                    #  POEM line + line ...
                    #  
                    print new_line  +"\n\n*******"
                    new_poem += new_line

                #print "\nLINE:",line,"\nNEW LINE:",new_line



            # 
            # WRITE new POEM TO FILE
            #
            txt_fn = html_file_number+".txt"
            print "TXT Filename: ", txt_fn.encode('utf-8')

            txt_fn_path = GENERATED_DIR+txt_fn
            print "txt_fn_path: ",txt_fn_path.encode('utf-8')


            if not os.path.exists(GENERATED_DIR):
                os.makedirs(GENERATED_DIR)

            f=open(txt_fn_path,'w+')

            dp = new_poem
            f.write(dp)

            f.close();
            
            #print new_poem





    

