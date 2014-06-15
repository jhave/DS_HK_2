"""

FAILED
ATTEMPT TO RESOLVE THE word space problem


UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)



USING the JSON file 
& BeautifulSoup

1.
retrieve the name of associated txt file 
containing the poem

2.
open the txt file

3. 
collect features

"""


DATA_DIR  =  "../../../../data/poetryFoundation/"

# "...._69.txt" contains only 69 files for testing
JSON_FILE  =  "json/poetryFoundation_JSON_69.txt"


from json import JSONDecoder
from functools import partial
from string import whitespace

#import nltk
from bs4 import BeautifulSoup

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




                soup = BeautifulSoup(open(txt_fn))
                #print str(soup)
                poem = soup.get_text()
                #print poem
                print type(poem)
                line_ipf = poem.split("\n")
                # NO EFFECT print text.strip(' \t\n\r')
            
                #& ANALYZE THE POEM
                i=0
                for ipf in line_ipf:

                    # get rid of all spaces... NOT WORKING!!! TRIED MANY SOLUTIONS...
                    # WORKS FOR MOST SPACES BUT LEAVES SOME HUGHE SPACES...
                    words = line_ipf[i].split()
                    line_no_indent=""
                    word_len=0

                   #print ipf

                    # for iws, word in enumerate(words):
                        
                    #     word_no_space =''.join(e for e in word if e.isalnum())
                    #     line_no_indent += word_no_space +' '   
                    #     word_len += len(word)
               
                    # if iws!=0:
                    #     print "words:", iws, "  avg word length:", word_len/iws , "line length:",len(line_no_indent),line_no_indent

                        
                print "# of lines:", ipf
