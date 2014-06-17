"""

USING the JSON file 

1.
retrieve the name of associated txt file 
containing the poem

2.
open the txt file

3. 
collect features

"""


from __future__ import division
import nltk, re, pprint
from nltk import Text


DATA_DIR  =  "../../../../data/poetryFoundation/"
# "...._69.txt" contains only 69 files for testing
JSON_FILE  =  "json/poetryFoundation_JSON_69.txt"


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
    for data in json_parse(infh):
        # process object 
        cnt=cnt+1
        print "poem:", cnt
        for idx, val in enumerate(data):
            # print idx, val
            # retrieve the name of associated txt file containing the poem
            if idx==0:
                txt_fn= DATA_DIR+"txt/"+val+".txt"
                print txt_fn

                # LOAD THE POEM HERE
                #
                # features
                # avg_line : avg line length 
                # avg_word : avg word length
                # avg_verse : avg word length
                # long_word : longest word
                #
                long_word=''
                avg_word=0
                avg_line=0
                avg_verse=0

                pf = open(txt_fn, 'rU')

                for line in pf:
                    print "line length:",len(line.strip()),"of",len(nltk.word_tokenize(line.strip())),"words:",line.strip()

                   
