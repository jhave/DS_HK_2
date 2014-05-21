"""
Beers
"""

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
beer = beer.dropna()
beer['Good'] = beer['WR'].apply(good)

# Original attempt

input = beer[ ['Reviews', 'ABV'] ].values
good = beer['Good'].values

score(input, good)

# Second attempt, with beer types

beer_types = ['Ale', 'Stout', 'IPA', 'Lager']

for t in beer_types:
	beer[t] = beer['Type'].str.contains(t) * 1

select = ['Reviews', 'ABV', 'Ale', 'Stout', 'IPA', 'Lager']
input = beer[select].values

score(input, good)

# Third attempt, with beer breweries

dummies = pd.get_dummies(beer['Brewery'])
input = beer[select].join(dummies.ix[:, 1:])

score(input, good)
