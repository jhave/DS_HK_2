#! /usr/bin/env python

"""

adapted from http://radimrehurek.com/2014/02/word2vec-tutorial/

a tutorial on how to use word2vec in gensim

NEXT step: "The word vectors can be also used for deriving word classes from huge data sets. This is achieved by performing K-means clustering on top of the word vectors." https://code.google.com/p/word2vec/
 
 API: http://radimrehurek.com/gensim/models/word2vec.html

 CYTHON bug makes training slow... so model is saved for reloading and analysis in another file.

Note: word2vec trains using skip-gram or CBOW
From Google Groups Milokov posts :
“Skip-gram: works well with small amount of the training data, represents well even rare words or phrases"

"""
 
import os
import sys

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim

DIR = "../../../../data/poetryFoundation/"

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
            	#print "LINE",line
               	yield line.split()


# a memory-friendly iterator
sentences = MySentences(DIR+'/txt/')

# words2vec
W2V_model = gensim.models.Word2Vec(sentences)

# save
W2V_model.save('tmp/W2V_model_vectors.bin')

# test...against google corpus
# http://radimrehurek.com/2014/02/word2vec-tutorial/
print W2V_model.accuracy('tmp/questions-words.txt')



########### OUTPUT ################################

########### using  yield line.split()
# 2014-06-16 09:55:35,186 : INFO : collected 122897 word types from a corpus of 991784 words and 155786 sentences
# 2014-06-16 09:55:35,239 : INFO : total 16728 word types after removing those with count<5
# 2014-06-16 09:55:35,240 : INFO : constructing a huffman tree from 16728 words
# 2014-06-16 09:55:35,895 : INFO : built huffman tree with maximum node depth 17

##########  yield line.split('\n')
# 2014-06-16 09:57:06,065 : INFO : collected 132554 word types from a corpus of 311543 words and 155786 sentences
# 2014-06-16 09:57:06,118 : INFO : total 114 word types after removing those with count<5
# 2014-06-16 09:57:06,118 : INFO : constructing a huffman tree from 114 words
# 2014-06-16 09:57:06,125 : INFO : built huffman tree with maximum node depth 10
#####################################################