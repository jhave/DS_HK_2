#! /usr/bin/env python
from collections import Counter

import re
from json import JSONDecoder
from functools import partial
from string import whitespace

#count words (not tokens, and not punctuation)
nonPunct = re.compile('.*[A-Za-z0-9].*')  # must contain a letter or digit
def countWords(str):
    filtered = [w for w in str if nonPunct.match(w)]
    counts = Counter(filtered)
    return sum(c for w,c in counts.iteritems())

def countChars(str):
    filtered = [w for w in str if nonPunct.match(w)]
    counts = Counter(filtered)
    if len(filtered)>0:
        return float(sum(len(w)*c for w,c in counts.iteritems())) / len(filtered)
    else:
        return 0.0
#count punctuation
def countPunctuation(str):
    filtered = [w for w in str if not nonPunct.search(w)]
    for w in str:
        
        np=nonPunct.match(w)
        # print w,np
        # if np:
        #     print np
        # else:
        #     print 'no match'
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


# correct errors in reading json
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
