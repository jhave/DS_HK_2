#!/usr/bin/env python

"""

Grab all BIOs.
Tag as POS.
Save lists of adjectives (ADJ), adverbs (ADV), foreign words (FW), interjection (UH)

"""

import json
import os,sys,random, datetime

import import_utilities

from pprint import pprint
import re
import codecs

import nltk

######################################################

DATA_DIR  =  "../../../../../data/poetryFoundation/"

READ_TXT_PATH = DATA_DIR+"ALL_poetryFoundation_BIO.txt"

READ_LIST_PATH = DATA_DIR+"NLTK_POS_LISTS_poetryFoundation_BIOs.txt"

# adjectives (JJ), adverbs (RB), foreign words (FW), interjection (UH)
JJ = []
RB = []
FW = []
UH = []
VBD = []
VBZ = []

num_of_files = 0
bio = ""
ALL_POS = ""

print "len(JJ):",len(JJ)




#################################################
#                                                 #
#   READ FILE
#                                                 #
#################################################

txt_data=open(READ_TXT_PATH).read()

auth_title_bio_ls = txt_data.split("~~~~!~~~")

c=0
for atb in auth_title_bio_ls:

    # testing limit...
    # c+=1
    # if c<6:

    author = atb.split('****!****')[0].strip(' \t\n\r')
    
    if len(atb.split('****!****'))==3:
        bio = atb.split('****!****')[2].strip(' \t\n\r')
        
        #print "\n________________________\n",
        print author,"\n________________________\n"
        token_tuples = nltk.word_tokenize(bio)
        
        tt = nltk.pos_tag(token_tuples)
        #print tt

        VBD += [i[0] for i in tt if i[1]=='VBD' ]
        VBD = list(set(VBD))
        #print "VBD:",VBD

        VBZ += [i[0] for i in tt if i[1]=='VBZ' and "\xe2" not in i[0] and not i[0].istitle()]
        #VBZ = list(set(VBZ))
        #print "VBZ:",VBZ

        if len(author.split(" "))>1:
            al=author.split(" ")[1]
        else:
            al=author.split(" ")[0]
        
        JJ += [i[0] for i in tt if i[1]=='JJ' and al not in i[0] and not import_utilities.isGarbageInWord_bool(i[0]) and len(i[0])>3 and not i[0].istitle() and import_utilities.strip_punctuation(i[0]) not in import_utilities.stopwords_ls and import_utilities.strip_punctuation(i[0]) not in import_utilities.personal_pronouns and "\xe2\x80\x94" not in i[0] and '\xc2\x96' not in i[0] and "-" not in i[0] and "\xe2\x80\x99" not in i[0] and "\xe2\x80\x9d" not in i[0] and "." not in i[0]]
        #ADJ = list(set(ADJ))
        #print "ADJ:",ADJ

        RB += [i[0] for i in tt if i[1]=='RB' and len(i[0])>5 and not i[0].istitle()]
        #ADV = list(set(ADV))
        #print "ADV:",ADV

        FW += [i[0] for i in tt if i[1]=='FW' ]
        #FW = list(set(FW))
        #print "FW:",FW

        UH += [i[0] for i in tt if i[1]=='UH' ]
        #UH = list(set(UH))
    #print "UH:",UH
    else:
        print "NO BIO*********************************************",author,len(atb.split('****!****'))


ALL_POS += "\nRB="+', '.join(RB)+"\n"
ALL_POS += "\nJJ="+', '.join(JJ)+"\n"
ALL_POS += "\nVBD="+', '.join(VBD)+"\n"
ALL_POS += "\nVBZ="+', '.join(VBZ)+"\n"
ALL_POS += "\nFW="+', '.join(FW)+"\n"
ALL_POS += "\nUH="+', '.join(UH)+"\n"

print ALL_POS

# #   &  ...
# #############################
# # STASH THE DATA           #
# #############################
txt_fn = "NLTK_POS_LISTS_poetryFoundation_BIOs.txt"
txt_fn_path = DATA_DIR+txt_fn
f_txt=open(txt_fn_path,'w')
f_txt.write(ALL_POS)       
f_txt.close();   
print "\nTXT file created at:",txt_fn_path


