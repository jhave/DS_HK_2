#! /usr/bin/env python

# Author: Mathieu Blondel
# License: BSD 3 clause

import numpy as np
import pylab as pl

from sklearn.linear_model import Ridge


def f(x):
    """ function to approximate by polynomial interpolation"""
    return x * np.sin(x)

# generate points used to plot
x_plot = np.linspace(0, 10, 100)

# generate points and keep a subset of them
x = np.linspace(0, 10, 100)
rng = np.random.RandomState(0)
rng.shuffle(x)
x = np.sort(x[:20])
y = f(x)

pl.plot(x_plot, f(x_plot), label="ground truth")
pl.scatter(x, y, label="training points")

for degree in [3, 4, 5]:
    ridge = Ridge()
    ridge.fit(np.vander(x, degree + 1), y)
    pl.plot(x_plot, ridge.predict(np.vander(x_plot, degree + 1)),
            label="degree %d" % degree)

pl.legend(loc='lower left')

pl.show()