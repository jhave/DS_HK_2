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
put into pandas df 

4. 
save as cvs

5. 
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

import nltk, re, pprint
from nltk import Text


DATA_DIR  =  "../../../../data/poetryFoundation/"
# "...._69.txt" contains only 69 files for testing
JSON_FILE  =  "json/poetryFoundation_JSON-COMPLETE_6.txt"


from json import JSONDecoder
from functools import partial
from string import whitespace

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
    '\xe2\x80\x99': '\'',	# apostrophe
    '\xe2\x80\x94': '--'	# em dash

}


# USAGE new_str = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, text)
def replace_chars(match):
    char = match.group(0)
    return chars[char]


def process_dob(poet_dob):

	birth = '0000'
	death = '0000'

	# empty
	if poet_dob == '':
		birth = '0000'
		death = '0000'

	# form "b. 1964"
	elif poet_dob.split(".")[0]=='b':
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
# Load JSON
#

with open(DATA_DIR+JSON_FILE, 'r') as infh:
    cnt=0 
    largest_word_ls=[]
    labels_ls=[]
    Author=''
    Title=''
    poet_DOB=''
    poem_dop=''
    
    # for every poem-file-object
    for data in json_parse(infh):
        # process object 
        cnt=cnt+1
        print "\n\n\ncnt:", cnt

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
                poem_dop = data[val.encode('utf-8')].encode('utf-8')
            elif val=='id':
                id=data[val.encode('utf-8')].encode('utf-8')
            elif val=='labels':
            	categories =data[val.encode('utf-8')]
            	for k,l in categories.iteritems():
            		cat_no_cruft = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, k)
            		for lid,lv in enumerate(l):
            			labels_ls.append(cat_no_cruft+"_"+lv.encode('utf-8'))
            		
        
        # make dob normal
        date_of_birth, date_of_death = process_dob(poet_dob)
        #print poet_dob,date_of_birth,date_of_death 

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

        for line in pf:

            i=i+1
            
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
	    print "id: ",id
	    print 'author',author
	    print 'title',title
	    print 'date_of_birth', date_of_birth
	    print 'date_of_death', date_of_death
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
	    print "largest_word_ls =", largest_word_ls
	    print "labels_ls =", labels_ls
    
        #data_dict["filename"] = val

    pf.close()

    print '[%s]' % ', '.join(map(str, largest_word_ls ))
