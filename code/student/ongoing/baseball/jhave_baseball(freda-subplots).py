"""
Questions & notes from Jhave: 
# QUESTION: why are the start values of Salary 0? -- they shouldn't be!
# QUESTION: how-to iterate over every column in train_X and plot it against train_y?
# mart suggested scatterplot matrices

Jhave's code is available as an Ipython Notebook here: 
http://nbviewer.ipython.org/github/jhave/DS_HK_2/blob/4e593295ae707e1f0749d143803e9805474eaab5/notebooks/baseball_PLOTS.ipynb

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import log

b2011 = pd.read_csv('../DS_HK_2/data/baseball/baseball_training_2011.csv')

fig = plt.figure()

x1 = log(b2011['G'])
x2 = log(b2011['AB'])
x3 = log(b2011['R'])
x4 = log(b2011['H'])
x5 = log(b2011['X2B'])
x6 = log(b2011['X3B'])
x7 = log(b2011['HR'])
x8 = log(b2011['RBI'])
x9 = log(b2011['SB'])
x10 = log(b2011['BB'])
x11 = log(b2011['IBB'])
x12 = log(b2011['HBP'])
x13 = log(b2011['SH'])
x14 = log(b2011['SF'])

y = log(b2011['salary'])

fig.add_subplot(441)
plt.scatter(x1, y)
plt.xlabel('Games')

fig.add_subplot(442)
plt.scatter(x2, y)
plt.xlabel('At Bats')

fig.add_subplot(443)
plt.scatter(x3, y)
plt.xlabel('Run')

fig.add_subplot(444) 
plt.scatter(x4, y)
plt.xlabel('Hit')

fig.add_subplot(445) 
plt.scatter(x5, y)
plt.xlabel('Doubles')

fig.add_subplot(446) 
plt.scatter(x6, y)
plt.xlabel('Triples')

fig.add_subplot(447)
plt.scatter(x7, y)
plt.xlabel('Homeruns')

fig.add_subplot(448)
plt.scatter(x8, y)
plt.xlabel('Runs Batted In')

fig.add_subplot(449)
plt.scatter(x9, y)
plt.xlabel('Stolen Bases')

fig.add_subplot(4, 4, 10)
plt.scatter(x10, y)
plt.xlabel('Base on Balls')

fig.add_subplot(4, 4, 11)
plt.scatter(x11, y)
plt.xlabel('Intentional walks')

fig.add_subplot(4, 4, 12)
plt.scatter(x12, y)
plt.xlabel('Hit by Pitch')

fig.add_subplot(4, 4, 13)
plt.scatter(x13, y)
plt.xlabel('Sacrifice Hits')

fig.add_subplot(4, 4, 14)
plt.scatter(x14, y)
plt.xlabel('Sacrifice Flies')

plt.show()