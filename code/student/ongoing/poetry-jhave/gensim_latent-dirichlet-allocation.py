"""

adapted from http://radimrehurek.com/gensim/wiki.html#latent-dirichlet-allocation

"""
 
import os
import sys

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim



DIR = "../../../../data/poetryFoundation/"

# iterator helper function
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
               yield line.split()


# a memory-friendly iterator
sentences = MySentences(DIR+'/txt/')


# LSI model
lsi = gensim.models.lsimodel.LsiModel(sentences, num_topics=400)