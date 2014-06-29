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

test_data_dir  =  "../../../../data/poetryFoundation/txt/"
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
        self.dictionary.filter_extremes(no_below=20,no_above=5, ) # check API docs for pruning params

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)

corpus = MyCorpus(test_data_dir) # create a dictionary

print "****************"
print "Create Tfidf model"
tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus] 

# limiter=0

num_topics = 120
num_clusters = 3
passes = 6

print "****************"
print "Create LDA model with",num_topics,"topics and",passes,"passes."
lda_model = LdaModel(corpus_tfidf , id2word=corpus.dictionary, num_topics=num_topics, passes=passes)
#lda_model = LdaModel(corpus, id2word=corpus.dictionary, num_topics=num_topics, passes=passes)
corpus_lda = lda_model[corpus]

# put topics into list
topics = [lda_model[c] for c in corpus_lda]

print "Done creating LDA model"
#print "# of documents:",file_cnt
print "# of topics:",len(topics)

#create a matrix of topics
dense = np.zeros((len(topics),num_topics),float)
for ti,t in enumerate(topics):
    for tj,v in t:
        dense[ti,tj] = v

pairwise = distance.squareform(distance.pdist(dense))

largest = pairwise.max()
for ti in range(len(topics)):
    pairwise[ti,ti]=largest+1

def closest_to(doc_id):
    return pairwise[doc_id].argmin()

counts = np.zeros(num_topics)
for doc_top in topics:
    for ti, _ in doc_top:
        counts[ti] += 1

top_words = lda_model.show_topic(counts.argmax(),64)
print "********** TOP Topics **************\n",top_words

bot_words = lda_model.show_topic(counts.argmin(),64)
print "\n********** BOTTOM Topics **************\n",bot_words

'''  OUTPUT 
################
****************
Create Tfidf model
2014-06-29 07:39:15,111 : INFO : collecting document frequencies
2014-06-29 07:39:15,171 : INFO : PROGRESS: processing document #0
2014-06-29 07:39:24,857 : INFO : PROGRESS: processing document #10000
2014-06-29 07:39:25,364 : INFO : calculating IDF weights for 10572 documents and 14957 features (1382824 matrix non-zeros)
****************
Create LDA model
2014-06-29 07:39:25,375 : INFO : using symmetric alpha at 0.025
2014-06-29 07:39:25,375 : INFO : using serial LDA version on this node
2014-06-29 07:39:25,470 : WARNING : input corpus stream has no len(); counting documents
2014-06-29 07:39:35,562 : INFO : running online LDA training, 40 topics, 2 passes over the supplied corpus of 10572 documents, updating model once every 2000 documents, evaluating perplexity every 10572 documents, iterating 50x with a convergence threshold of 0.001000

Done creating LDA model
# of topics: 10572
[(0.044971196193106404, u'walter'), (0.033857771559132138, u'blackbird'), (0.030081817876806752, u'tuesday'), (0.019250428368620807, u'honey'), (0.01920635860410929, u'jump'), (0.018870315284757345, u'tiled'), (0.018735216192208779, u'redness'), (0.0164715094774672, u'font'), (0.015488979088015662, u'los'), (0.014744857501364428, u'unlocked'), (0.012933344997127583, u'radiating'), (0.010758599432322434, u'las'), (0.010141205427305292, u'portent'), (0.0090601586702265986, u'twitter'), (0.0076200111500862658, u'back'), (0.0056493265918978455, u'lark'), (0.003415531986339745, u'spike'), (0.0033336421122233178, u'all'), (0.0032546667732631369, u'her'), (0.0030653222309496822, u'swerve'), (0.0026579240718903529, u'pokes'), (0.002518185149964589, u'prais'), (0.00239550550451762, u'piped'), (0.0023847649822997235, u'by'), (0.0023098680159543048, u'from'), (0.002291122724880522, u'huh'), (0.0022714941353645093, u'not'), (0.0021912195182074755, u'an'), (0.0021401110302398047, u'me'), (0.002089301509778613, u'he'), (0.0020105389624886587, u'my'), (0.0020080438069683066, u'spikes'), (0.0019273422765391823, u'but'), (0.0019030078825918251, u'which'), (0.0018731488807780356, u'sun'), (0.0018100779380983861, u'so'), (0.0017875242177813728, u'their'), (0.001777452674147587, u'there'), (0.0017130115668347011, u'you'), (0.0016706783869216923, u'was'), (0.0016680678413145071, u'saplings'), (0.0016260089028658235, u'when'), (0.001616744680180041, u'what'), (0.0015985824854574018, u'she'), (0.0015536439968981419, u'woodlands'), (0.0015363235172487408, u'love'), (0.0015177113522258929, u'day'), (0.0015094064002848821, u'sweet'), (0.0014737843341979813, u'as'), (0.0014702722138900414, u'his'), (0.001366195091573935, u'this'), (0.001342231609789133, u'up'), (0.0013290053578830471, u'they'), (0.0013067737780795027, u'leaves'), (0.0012954637247979816, u'd'), (0.0012824206459958775, u'now'), (0.001281156632788569, u'are'), (0.0012721295287890753, u'at'), (0.0012632189734084116, u'be'), (0.0012507666434839544, u'no'), (0.0012376434306362869, u'water'), (0.0012320362481780841, u'through'), (0.0012239084266102347, u'clicking'), (0.0011978341864856482, u'light')]


###########
########### ANOTHR RUN
###########

2014-06-29 14:13:14,287 : INFO : adding document #0 to Dictionary(0 unique tokens: [])
2014-06-29 14:13:24,013 : INFO : adding document #10000 to Dictionary(82249 unique tokens: [u'fawn', u'lenitives', u'schlegel', u'nunnery', u'chthonic']...)
2014-06-29 14:13:24,522 : INFO : built Dictionary(84732 unique tokens: [u'fawn', u'lenitives', u'schlegel', u'nunnery', u'chthonic']...) from 10572 documents (total 3061627 corpus positions)
2014-06-29 14:13:24,558 : INFO : keeping 14958 tokens which were in no less than 10 and no more than 6343 (=60.0%) documents
2014-06-29 14:13:24,612 : INFO : resulting dictionary: Dictionary(14958 unique tokens: [u'fawn', u'raining', u'hordes', u'colony', u'yellow']...)
****************
Create Tfidf model
2014-06-29 14:13:24,612 : INFO : collecting document frequencies
2014-06-29 14:13:24,667 : INFO : PROGRESS: processing document #0
2014-06-29 14:13:33,810 : INFO : PROGRESS: processing document #10000
2014-06-29 14:13:34,337 : INFO : calculating IDF weights for 10572 documents and 14957 features (1382824 matrix non-zeros)
****************
Create LDA model
2014-06-29 14:13:34,348 : INFO : using symmetric alpha at 0.0125
2014-06-29 14:13:34,348 : INFO : using serial LDA version on this node
2014-06-29 14:13:34,545 : WARNING : input corpus stream has no len(); counting documents
2014-06-29 14:13:44,460 : INFO : running online LDA training, 80 topics, 10 passes over the supplied corpus of 10572 documents, updating model once every 2000 documents, evaluating perplexity every 10572 documents, iterating 50x with a convergence threshold of 0.001000
2014-06-29 14:13:47,057 : INFO : PROGRESS: pass 0, at document #2000/10572
2014-06-29 14:13:57,295 : INFO : merging changes from 2000 documents into a model of 10572 documents

Done creating LDA model
# of topics: 10572
[(0.012248812706737775, u'from'), (0.011275572757831509, u'as'), (0.009931429152605491, u'like'), (0.0096481801978632979, u'at'), (0.0078726042370603246, u'into'), (0.0075650043145078782, u'by'), (0.0071149003413884873, u'out'), (0.0070248262648561393, u'its'), (0.0070221120602819414, u'their'), (0.0061476469976050633, u'an'), (0.0059782149123324638, u'up'), (0.005412499438804644, u'or'), (0.0053072336354727349, u'one'), (0.0051397592379505835, u'over'), (0.0050451476931827298, u'through'), (0.0049160457128866334, u'down'), (0.0046101981214220879, u'his'), (0.0043406787121099471, u'where'), (0.00397974511246817, u'back'), (0.0039215631119906488, u'this'), (0.0034603026715559542, u'all'), (0.003302886346227565, u'then'), (0.0032945941406953157, u'water'), (0.003229466079556838, u'black'), (0.0030866128065683341, u'my'), (0.0030739715376817446, u'they'), (0.0030235957745933656, u'no'), (0.0029810347915479748, u'was'), (0.0028863951408793108, u'light'), (0.0028644591772195322, u'each'), (0.0028515683336252508, u'off'), (0.0027071146985327013, u'there'), (0.0026756373685744026, u'white'), (0.0026238775974655871, u'two'), (0.002557616573365235, u'who'), (0.0025547958775027661, u'not'), (0.0025500850507868831, u'when'), (0.0024501809346121214, u'them'), (0.0024364074928425118, u'but'), (0.0024303533683145643, u'under'), (0.0023272907354147387, u'blue'), (0.0022596412786312046, u'so'), (0.0022389037952815394, u'across'), (0.0021272862903940169, u'air'), (0.0021224945389856443, u'between'), (0.0020886076668701179, u'hand'), (0.001990428916719621, u'eyes'), (0.0019253618239914966, u'red'), (0.0019250116231761404, u'old'), (0.0019142533084925053, u'against'), (0.0019025583501115155, u'now'), (0.0018770569043935702, u'what'), (0.0018745376520513178, u'behind'), (0.001868650613137519, u'time'), (0.0018635104667978479, u'were'), (0.0018619554372475424, u'long'), (0.0018295257343513697, u'hands'), (0.0018251489310097922, u'before'), (0.0017576844247555584, u'head'), (0.001757456458736288, u'small'), (0.0017553437291808484, u'after'), (0.0017467180816964753, u'around'), (0.0017353429217779558, u'dark'), (0.0017277349177820108, u'man')]
[Finished in 662.1s]
'''
