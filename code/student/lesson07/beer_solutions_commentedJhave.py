"""
Beers
"""
import pandas as pd
from sklearn import linear_model, metrics

logm = linear_model.LogisticRegression()

def score(input, response):
  logm.fit(input, response)
  score = logm.score(input, good)
  print 'R^2 Score : %.03f' % (score)

def good(x):
  if x > 4.3:
    return 1
  else: 
    return 0

url = 'http://www-958.ibm.com/software/analytics/manyeyes/datasets/af-er-beer-dataset/versions/1.txt'

beer = pd.read_csv(url, delimiter="\t")
print beer.head()
beer = beer.dropna()
beer['Good'] = beer['WR'].apply(good)

# Original attempt

input = beer[ ['Reviews', 'ABV'] ].values
good = beer['Good'].values

score(input, good)

# Second attempt, with beer types

beer_types = ['Ale', 'Stout', 'IPA', 'Lager']

# to put in new table columns and do comparison in a single loop using List instantiated above
for t in beer_types:
	beer[t] = beer['Type'].str.contains(t) * 1

select = ['Reviews', 'ABV', 'Ale', 'Stout', 'IPA', 'Lager']
input = beer[select].values

score(input, good)

# Third attempt, with beer breweries

# sparse density means that the set of values contain lots of zeros that are dummy variables
# as in this case where a brewery might make only a few beers but there are many beers made...
# get_dummies "Convert categorical variable into dummy/indicator variables"
# sparse can be problematic, if the data expands and introduces.
dummies = pd.get_dummies(beer['Brewery'])

# beer join with dummies... all rows [:] but only from 2nd column onwards [ ,1:]
# model can no longer distinguish, one of th columns needs to be removed...
# in this example we have 104 dummy columns, drop one, to make sure that the logistic regression can make sure 
# trail test removing one column...
# in crucial cases drop the column which is least predictive using trails
input = beer[select].join(dummies.ix[:, 1:]
)
  
# 
score(input, good)
