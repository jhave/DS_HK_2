#!/usr/bin/env python
"""

LESSON 06 Regression

"""

import pandas as pd
import numpy as np

from sklearn import feature_selection
import matplotlib.pyplot as plt


cars = pd.read_csv("cars.csv")
##print cars.head()

plt.scatter(cars["speed"],cars["dist"])



