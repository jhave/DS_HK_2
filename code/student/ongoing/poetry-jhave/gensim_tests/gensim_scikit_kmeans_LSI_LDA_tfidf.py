#!/usr/bin/env python

"""
adapted from: https://gist.github.com/balamuru/4756543
gensim_scikit_kmeans.py

gensim + scikit clustering vs scipy clustering (DEBUG)

"""

import operator

import logging
from scipy.odr import models
from sklearn import metrics
import unittest
import os
import os.path
import tempfile

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

from sklearn.cluster import KMeans
from gensim.matutils import corpus2dense
import gensim
import logging

from gensim.corpora import mmcorpus, Dictionary
from gensim.models import lsimodel, ldamodel, tfidfmodel, rpmodel, logentropy_model, TfidfModel, LsiModel, LdaModel
from gensim import matutils,corpora

from gensim import similarities
from time import time
 
t0=time()


from scipy.cluster.vq import kmeans,vq

test_data_dir  =  "../../../../../data/poetryFoundation/txt/"
file_cnt=60


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    #print "ITER"
    for root, dirs, files in os.walk(top_directory):
        #print root
        
        for file in filter(lambda file: file.endswith('.txt'), files):
            #print file
            #file_cnt=file_cnt+1
            # read the entire document, as one big string
            document = open(os.path.join(root, file)).read() 
            # or whatever tokenization suits you
            yield gensim.utils.tokenize(document, lower=True) 

class MyCorpus(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        
        """
        ... Stop words removed using .filter_extremes
        Filter out tokens that appear in

            less than no_below documents (absolute number) or
            more than no_above documents (fraction of total corpus size, not absolute number).
        
        """
        self.dictionary.filter_extremes(no_below=10,no_above=0.6, ) # check API docs for pruning params

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)

corpus = MyCorpus(test_data_dir) # create a dictionary
#print("Corpus:",MyCorpus)
# for vector in corpus: # convert each document to a bag-of-word vector
#      print vector

#numpy_matrix = gensim.matutils.corpus2dense(corpus, corpus.topics)


print "****************"
print "Create Tfidf model"
tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus] 

limiter=0

# SORTING ATTEMPTS 
# does NOT work, error:                         corpus_tfidf.sort()   
#                                               corpus_tfidf.sort(key=operator.itemgetter(1))
# SORTS on first index                          sorted(corpus_tfidf, reverse=True)
# IndexError: list index out of range           sorted(corpus_tfidf, key=lambda x: x[0])


# for doc in corpus_tfidf:
#     if limiter < 100: 
#         print "limiter:",limiter,"\n",doc
#     for dw in doc:
#         limiter+=1
#         if limiter < 100:
#             print dw,corpus.dictionary[dw[0]]



num_topics = 40
num_clusters = 3
passes = 2


print "****************"
print "Create LDA model"
#lda_model = LdaModel(corpus_tfidf , id2word=corpus.dictionary, num_topics=num_topics, passes=passes)
lda_model = LdaModel(corpus, id2word=corpus.dictionary, num_topics=num_topics, passes=passes)
corpus_lda = lda_model[corpus]

# put topics into list
topics = [lda_model[c] for c in corpus_lda]

print "Done creating LDA model"
#print "# of documents:",file_cnt
print "# of topics:",len(topics)

#create a matrix of topics
dense = np.zeros((len(topics),100),float)
for ti,t in enumerate(topics):
    for tj,v in t:
        dense[ti,tj] = v

pairwise = distance.squareform(distance.pdist(dense))

largest = pairwise.max()
for ti in range(len(topics)):
    pairwise[ti,ti]=largest+1

def closest_to(doc_id):
    return pairwise[doc_id].argmin()

counts = np.zeros(100)
for doc_top in topics:
    for ti, _ in doc_top:
        counts[ti] += 1

words = lda_model.show_topic(counts.argmax(),64)
print words


#
# plot
#

# for ti in xrange(84):
#     words = lda_model.show_topic(ti, 64)
#     tf = sum(f for f, w in words)
#     print('\n'.join('{}:{}'.format(w, int(1000. * f / tf)) for f, w in words))
#     print()
#     print()
#     print()

# thetas = [lda_model[c] for c in corpus_lda]
# plt.hist([len(t) for t in thetas], np.arange(42))
# plt.title('LDA #1')
# plt.ylabel('Nr of documents')
# plt.xlabel('Nr of topics')
# plt.show()
# plt.savefig('LDA.png')

# model1 = LdaModel(
#     corpus_lda, num_topics=100, id2word=corpus.dictionary, alpha=1.)
# thetas1 = [model1[c] for c in corpus]

# #model8 = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=corpus.id2word, alpha=1.e-8)
# #thetas8 = [model8[c] for c in corpus]
# plt.clf()
# plt.hist([[len(t) for t in thetas], [len(t) for t in thetas1]], np.arange(42))
# plt.title('LDA #2')
# plt.ylabel('Nr of documents')
# plt.xlabel('Nr of topics')
# plt.text(9, 223, r'default alpha')
# plt.text(26, 156, 'alpha=1.0')
# plt.show()
# plt.savefig('LDA_1.png')




# print "****************"
# print "Create LSI model"
# #lsi_model = LsiModel(corpus_tfidf , id2word=corpus.dictionary, num_topics=num_topics)
# lsi_model = LsiModel(corpus, id2word=corpus.dictionary, num_topics=topics)
# corpus_lsi = lsi_model[corpus]



# print "*********************"
# print "\n\nPrint LSI model\n"
# topic_id = 0
# for topic in lsi_model.show_topics(num_words=3):
#     # print "TOPIC (LSI2) " + str(topic_id) + " : " + topic
#     print topic
#     topic_id+=1



# #for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
# #   print "Doc " + str(doc)

# corpus_lsi_dense = corpus2dense(corpus_lsi, topics)
# print "Dense Matrix Shape " + str(corpus_lsi_dense.shape)

# max_iter_k=100
# n_init_k = 5
# init_k='random'
# print "********** \n scikit integration  max_iter=",max_iter_k," n_inits=",n_init_k
# km = KMeans(num_clusters, init_k, max_iter_k, n_init_k, verbose=0)
# km.fit(corpus_lsi_dense)

# num_k_clusters = 6
# print "computing K-Means with K = ",num_k_clusters, " clusters"
# centroids,_ = kmeans(corpus_lsi_dense,num_k_clusters)
# # assign each sample to a cluster
# idx,_ = vq(corpus_lsi_dense,centroids)

# # some plotting using numpy's logical indexing
# plot(
#     corpus_lsi_dense[idx==0,0],corpus_lsi_dense[idx==0,1],'ob',
#     corpus_lsi_dense[idx==1,0],corpus_lsi_dense[idx==1,1],'or',
#     corpus_lsi_dense[idx==2,0],corpus_lsi_dense[idx==2,1],'og',
#     corpus_lsi_dense[idx==3,0],corpus_lsi_dense[idx==3,1],'xr'
# )

# plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
# show()

# #print str(km.labels_)
# labels = km.labels_      #<============WRONG
# print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_)
# print "Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_)
# print "V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_)
# print "Adjusted Rand-Index: %.3f" %\
#      metrics.adjusted_rand_score(labels, km.labels_)
# print "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(
#    corpus_lsi_dense, labels, sample_size=100)

# print

