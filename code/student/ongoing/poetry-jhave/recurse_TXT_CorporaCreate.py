#! /usr/bin/env python

# BASED ON https://github.com/piskvorky/gensim/wiki/Recipes-&-FAQ

import os
import sys

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim
#from gensim import corpora, models, similarities

DIR = "../../../../data/poetryFoundation/poem/"

def iter_documents(DIR):
    print "AHA iter_documents called "+DIR
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(DIR):
        for file in files:
            
            document = open(os.path.join(root, file)).read() # read the entire document, as one big string
            yield gensim.utils.tokenize(document, lower=True) # or whatever tokenization suits you


class MyCorpus(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        self.dictionary.filter_extremes(no_below=1, keep_n=30000) # check API docs for pruning params

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)



corpus = MyCorpus(DIR) # create a dictionary
#for vector in corpus: # convert each document to a bag-of-word vector
   # print vector

"""
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
"""