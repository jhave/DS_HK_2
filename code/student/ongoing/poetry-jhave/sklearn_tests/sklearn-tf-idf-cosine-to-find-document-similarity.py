#! /usr/bin/env python

"""
from: http://stackoverflow.com/questions/12118720/python-tf-idf-cosine-to-find-document-similarity

if you want to extract count features and apply TF-IDF normalization and row-wise euclidean normalization you can do it in one operation with TfidfVectorizer:

"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups

from sklearn.metrics.pairwise import linear_kernel

twenty = fetch_20newsgroups()
#print twenty.head()

print "_____________"

tfidf = TfidfVectorizer().fit_transform(twenty.data)

print "tfidf:",tfidf

"""
Now to find the cosine distances of one document (e.g. the first in the dataset) and all of the others you just need to compute the dot products of the first vector with all of the others as the tfidf vectors are already row-normalized. The scipy sparse matrix API is a bit weird (not as flexible as dense N-dimensional numpy arrays). To get the first vector you need to slice the matrix row-wise to get a submatrix with a single row:

tfidf[0:1]

scikit-learn already provides pairwise metrics (a.k.a. kernels in machine learning parlance) that work for both dense and sparse representations of vector collections. In this case we need a dot product that is also known as the linear kernel:
"""

cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
cosine_similarities
print "cosine_similarities:", cosine_similarities

"""
Hence to find the top 5 related documents, we can use argsort and some negative array slicing (most related documents have highest cosine similarity values, hence at the end of the sorted indices array):
"""
related_docs_indices = cosine_similarities.argsort()[:-5:-1]
print "RELATED DOC INDICES",related_docs_indices

print "cosine_similarities[related_docs_indices]", cosine_similarities[related_docs_indices]
