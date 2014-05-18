#!/usr/bin/python
# Import required libraries
import timeit as t
from numpy import *

print "timing the speed of my vector matrix multiply versus numpy dot"

"""
dot speed: 0.7672370016137506
my def speed: 0.9984355096211438

"""

matr = [ [1, 2, 3, 4], 
           [5, 6, 7, 8],
           [9, 0, 1, 2] ]

vect = [1 ,2, 3]


print "\n\n timing dot\n\n"
t.timeit('dot(vect, matr)', setup="from __main__ import dot, matr, vect", 
         number = 100000)

print "\n\n timing my own version\n\n"


def vectorMatrixMultiply(vect,matr):
    return [sum(matr[j][i]*vect[j] for j in range(len(vect))) for i in range(len(matr[0]))] 

# timeit
t.timeit('vectorMatrixMultiply(vect,matr)', setup="from __main__ import vectorMatrixMultiply, vect, matr",  
         number = 100000)         