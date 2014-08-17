#!/usr/bin/env python

import sys
import random
from random import choice



DATA_DIR  =  "../../../../data/poetryFoundation/"


def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    
    chain = {}
    words = corpus.split()
    
    for i in range(len(words)-2):
        pair = (words[i], words[i+1])
        if (pair in chain):
            chain[pair] += [ words[i+2] ]
        else:
            chain[pair] = [ words[i+2] ]
    #print chain    
    return chain

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    # To start, we want a word that starts with a capital letter
    # start = 'z'
    # while (start[0][0] != start[0][0].upper()):
    #     
    start = random.choice(chains.keys())
    
    line = list(start)
    
    last = line[-1][-1]
    linLen = 60#random.randint(2,5)
    while (len(line) < linLen):
        #linLen = random.randint(12,40)
        # while (not line[-1][-1] in ['.','?']):
    	next = chains[tuple(line[-2:])]
    	line += [ choice(next) ]
#    	print "line: %r" % line
    
    #print "line: %r" % line
    cnt=0
    lineated=""
    for w in line:
        cnt=cnt+1
        lineated+=w+" "
        if cnt>3:
            cnt=0
            lineated+="\n"
    

    return lineated
    return " ".join(line)

def main():
    args = sys.argv
    #filename = args[1]
    filename = "bernstein_rough-trades+dark-city.txt"#bernstein_rough-trades.txt"#DATA_DIR+"ALL/ALL_poetryFoundation_POEMS.txt"#'lyrics.txt'

    # Change this to read input_text from a file
    f = open(filename, "r")
    chain_dict = make_chains(f.read())

    for i in range(20):
        for i in range(320):
            print make_text(chain_dict)
        print ""

    # allWORDS=""
    # allWORDS = make_text(chain_dict)
    # print allWORDS

    #print make_text(chain_dict)

    # break it down into lines
    # linLen=4
    # ln=0
    # for w in allWORDS:
    #     ln=ln+1
    #     if ln<linLen:
    #         print w
    #     else:
    #         print "\n"

            
#    random_text = make_text(chain_dict)
#    print random_text

if __name__ == "__main__":
    main()
