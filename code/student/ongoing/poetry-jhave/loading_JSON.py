"""

USING the JSON file 

1.
retrieve the name of associated txt file 
containing the poem


"""


DATA_DIR  =  "../../../../data/poetryFoundation/"
JSON_FILE  =  "json/poetryFoundation_JSON_69.txt"


from json import JSONDecoder
from functools import partial
from string import whitespace

#import nltk


def json_parse(fileobj, decoder=JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
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

                with open(txt_fn, 'r') as poem_file:
                    # & ANALYZE THE POEM
                    i=0
                    for ipf,line_ipf in enumerate(poem_file):
                        # get rid of all spaces... NOT WORKING!!! TRIED MANY SOLUTIONS...
                        # WORKS FOR MOST SPACES BUT LEAVES SOME HUGHE SPACES...
                        words = line_ipf.split()
                        line_no_indent=""
                        word_len=0
                        for iws, word in enumerate(words):
                            word = word.strip(' \t\n\r')
                            line_no_indent += word +' '   
                            word_len += len(word)
                            # not working .translate(None, whitespace)+' '

                        if iws !=0:
                            print "words:", iws, "     avg word length", word_len/iws ,len(line_no_indent), line_no_indent    
                            # not working .lstrip(' ')
                    print "# of lines:", ipf

                # fh = open(txt_fn, "r")
                # lines = fh.readlines()
                # fh.close()
                # # Weed out blank lines with filter
                # lines = filter(lambda x: not x.isspace(), lines)
                # for i,line in enumerate(lines):
                #     print len(line), line
                # print "# of lines:", i
                # PUT RESULT from poems INTO ONE BIG NUMPY ARRAY?
                # OR CLUSTER POEMS BY AUTHOR?
                #
                #
                # OR CORRELATE IT WITH RESULTS ACHIEVED BY SERIALIZING PROCESS ON ENTIRE CORPUS IN GENSIM ???
                # 

