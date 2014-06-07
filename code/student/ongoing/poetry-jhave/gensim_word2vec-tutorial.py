"""

adapted from http://radimrehurek.com/2014/02/word2vec-tutorial/

a tutorial on how to use word2vec in gensim

NEXT step: "The word vectors can be also used for deriving word classes from huge data sets. This is achieved by performing K-means clustering on top of the word vectors." https://code.google.com/p/word2vec/
 
 API: http://radimrehurek.com/gensim/models/word2vec.html

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
               yield line.split()


# a memory-friendly iterator
sentences = MySentences(DIR+'/txt/')

# words2vec
W2V_model = gensim.models.Word2Vec(sentences)


