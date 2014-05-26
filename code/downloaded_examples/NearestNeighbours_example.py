#!/usr/bin/python
# Import required libraries

from sklearn.neighbors import NearestNeighbors
import numpy as np

"""
Because the query set matches the training set, the nearest neighbor of each point is the point itself, at a distance of zero.
"""
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])

nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)

distances, indices = nbrs.kneighbors(X)
print "distances\n",distances
print "\nindices\n",indices

nbrs.kneighbors_graph(X).toarray()