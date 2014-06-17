"""
adapted from: https://gist.github.com/balamuru/4756543
gensim_scikit_kmeans.py

gensim + scikit clustering vs scipy clustering (DEBUG)

"""

import logging
from scipy.odr import models
from sklearn import metrics
import unittest
import os
import os.path
import tempfile

import numpy
from matplotlib.pyplot import plot, show
from sklearn.cluster import KMeans
from gensim.matutils import corpus2dense
import gensim
import logging

from gensim.corpora import mmcorpus, Dictionary
from gensim.models import lsimodel, ldamodel, tfidfmodel, rpmodel, logentropy_model, TfidfModel, LsiModel
from gensim import matutils,corpora

from scipy.cluster.vq import kmeans,vq

test_data_dir  =  "../../../../data/poetryFoundation/txt/"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            #print file
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

corpus = MyCorpus(test_data_dir) # create a dictionary
for vector in corpus: # convert each document to a bag-of-word vector
    print vector

topics = 200
num_clusters = 4

print "Create models"
lsi_model = LsiModel(corpus, id2word=corpus.dictionary, num_topics=topics)
corpus_lsi = lsi_model[corpus]

print "Done creating models"


#lsi_model_2 .print_topics(5)

topic_id = 0
for topic in lsi_model.show_topics(num_words=5):
    print "TOPIC (LSI2) " + str(topic_id) + " : " + topic
    topic_id+=1


#for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#    print "Doc " + str(doc)


corpus_lsi_dense = corpus2dense(corpus_lsi, topics)
print "Dense Matrix Shape " + str(corpus_lsi_dense.shape)


#attempt scikit integration
km = KMeans(num_clusters, init='random', max_iter=100, n_init=1, verbose=1)
km.fit(corpus_lsi_dense)


#attempt scipy integration
# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(corpus_lsi_dense,6)
# assign each sample to a cluster
idx,_ = vq(corpus_lsi_dense,centroids)

# some plotting using numpy's logical indexing
plot(
    corpus_lsi_dense[idx==0,0],corpus_lsi_dense[idx==0,1],'ob',
    corpus_lsi_dense[idx==1,0],corpus_lsi_dense[idx==1,1],'or',
    corpus_lsi_dense[idx==2,0],corpus_lsi_dense[idx==2,1],'og',
    corpus_lsi_dense[idx==3,0],corpus_lsi_dense[idx==3,1],'xr'
)

plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()

#print str(km.labels_)
labels = km.labels_      #<============WRONG
print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_)
print "Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_)
print "V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_)
print "Adjusted Rand-Index: %.3f" %\
     metrics.adjusted_rand_score(labels, km.labels_)
print "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(
   corpus_lsi_dense, labels, sample_size=100)

print



""" ************ OUTPUT ******************

2014-06-07 12:41:30,260 : INFO : adding document #0 to Dictionary(0 unique tokens: [])
2014-06-07 12:41:30,415 : INFO : built Dictionary(5702 unique tokens: [u'yellow', u'four', u'woods', u'hanging', u'crooned']...) from 69 documents (total 26692 corpus positions)
2014-06-07 12:41:30,421 : INFO : keeping 5679 tokens which were in no less than 1 and no more than 34 (=50.0%) documents
2014-06-07 12:41:30,434 : INFO : resulting dictionary: Dictionary(5679 unique tokens: [u'yellow', u'four', u'woods', u'hanging', u'crooned']...)
[(0, 1), (41, 2), (87, 1), (147, 1), (209, 1), (239, 1), (240, 2), (295, 2), (304, 2), (440, 1), (578, 2), (647, 1), (759, 1), (790, 1), (862, 1), (927, 3), (1077, 1), (1090, 1), (1094, 1), (1190, 1), (1246, 1), (1247, 1), (1293, 1), (1422, 1), (1474, 3), (1543, 6), (1589, 1), (1612, 2), (1625, 1), (1638, 1), (1668, 1), (1783, 1), (1792, 1), (1805, 1), (1856, 1), (1899, 1), (1900, 2), (1922, 1), (1954, 1), (1970, 1), (1985, 1), (2025, 1), (2182, 1), (2247, 1), (2286, 2), (2342, 1), (2385, 1), (2404, 1),....
Create models
2014-06-07 12:41:30,970 : INFO : using serial LSI version on this node
2014-06-07 12:41:30,970 : INFO : updating model with new documents
2014-06-07 12:41:31,167 : INFO : preparing a new chunk of documents
2014-06-07 12:41:31,174 : INFO : using 100 extra samples and 2 power iterations
2014-06-07 12:41:31,174 : INFO : 1st phase: constructing (5679, 300) action matrix
2014-06-07 12:41:31,187 : INFO : orthonormalizing (5679, 300) action matrix
2014-06-07 12:41:32,157 : INFO : 2nd phase: running dense svd on (300, 69) matrix
2014-06-07 12:41:32,224 : INFO : computing the final decomposition
2014-06-07 12:41:32,224 : INFO : keeping 60 factors (discarding 0.000% of energy spectrum)
2014-06-07 12:41:32,289 : INFO : processed documents up to #69
2014-06-07 12:41:32,292 : INFO : topic #0(286.629): 0.394*"her" + 0.316*"your" + 0.259*"you" + 0.193*"he" + 0.176*"or" + 0.175*"she" + 0.166*"my" + 0.144*"naomi" + 0.143*"we" + 0.134*"me"
2014-06-07 12:41:32,293 : INFO : topic #1(134.555): 0.703*"we" + 0.275*"was" + 0.275*"stick" + 0.258*"were" + -0.151*"her" + 0.142*"us" + 0.133*"what" + 0.128*"city" + -0.116*"your" + 0.109*"song"
2014-06-07 12:41:32,295 : INFO : topic #2(79.714): 0.782*"say" + 0.202*"you" + 0.147*"love" + 0.145*"o" + 0.129*"my" + 0.127*"am" + -0.085*"naomi" + -0.082*"she" + 0.082*"your" + 0.080*"his"
2014-06-07 12:41:32,296 : INFO : topic #3(52.570): -0.444*"you" + -0.333*"same" + 0.263*"say" + 0.217*"stick" + -0.198*"are" + 0.130*"was" + -0.125*"can" + -0.119*"will" + 0.118*"her" + -0.109*"re"
2014-06-07 12:41:32,298 : INFO : topic #4(48.309): -0.492*"stick" + 0.249*"we" + -0.235*"you" + -0.210*"city" + 0.195*"again" + 0.187*"beginning" + -0.148*"as" + -0.142*"song" + 0.119*"new" + 0.117*"had"
Done creating models
TOPIC (LSI2) 0 : 0.394*"her" + 0.316*"your" + 0.259*"you" + 0.193*"he" + 0.176*"or"
TOPIC (LSI2) 1 : 0.703*"we" + 0.275*"was" + 0.275*"stick" + 0.258*"were" + -0.151*"her"
TOPIC (LSI2) 2 : 0.782*"say" + 0.202*"you" + 0.147*"love" + 0.145*"o" + 0.129*"my"
TOPIC (LSI2) 3 : -0.444*"you" + -0.333*"same" + 0.263*"say" + 0.217*"stick" + -0.198*"are"
TOPIC (LSI2) 4 : -0.492*"stick" + 0.249*"we" + -0.235*"you" + -0.210*"city" + 0.195*"again"
...
...
Dense Matrix Shape (200, 69)
Initialization complete
Iteration  0, inertia 129867.999
Iteration  1, inertia 128701.005
Iteration  2, inertia 121562.750
Iteration  3, inertia 93075.843
Iteration  4, inertia 71782.192
Iteration  5, inertia 46523.137
Iteration  6, inertia 46424.133
Iteration  7, inertia 46342.424
Iteration  8, inertia 46294.283
Iteration  9, inertia 46239.472
Converged at iteration 9
Homogeneity: 1.000
Completeness: 1.000
V-measure: 1.000
Adjusted Rand-Index: 1.000
Silhouette Coefficient: 0.582

[Finished in 11.0s]
"""