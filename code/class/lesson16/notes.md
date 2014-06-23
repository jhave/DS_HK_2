# Data Exploration and Diagnostics

Working though the baseball regression problem.

## Domain Knowlegde. You can't tell your SH from your SFs? Time for some Baseball 101!

* *Number of home runs*: Number of home runs People want to see home : People want to
see home runs—home runs are exciting, and teams will pay for players who can hit
home runs
* *Batting average* (Hits/At Bats): Most common statistic when comparing players
* *Slugging percentage* (Total Bases/At Bats):  Measures the average number of
bases a player

*[Baseball Statistics](http://en.wikipedia.org/wiki/Baseball_statistics)*

## Available features

    lahmanID, Unique number assigned to each player
    playerID, A unique code asssigned to each player.  The playerID links the data in this file with records in the other files.
    managerID, An ID for individuals who served as managers
    hofID, An ID for individuals who are in teh baseball Hall of Fame
    birthYear, Year player was born
    birthMonth, Month player was born
    birthDay, Day player was born
    birthCountry, Country where player was born
    birthState, State where player was born
    birthCity, City where player was born
    deathYear, Year player died
    deathMonth, Month player died
    deathDay, Day player died
    deathCountry, Country where player died
    deathState, State where player died
    deathCity, City where player died
    nameFirst, Player's first name
    nameLast, Player's last name
    nameNote, Note about player's name (usually signifying that they changed their name or played under two differnt names)
    nameGiven, Player's given name (typically first and middle)
    nameNick, Player's nickname
    weight, Player's weight in pounds
    height, Player's height in inches
    bats, Player's batting hand (left, right, or both)
    throws, Player's throwing hand (left or right)
    debut, Date that player made first major league appearance
    finalGame, Date that player made first major league appearance (blank if still active)
    college, College attended
    lahman40ID, ID used in Lahman Database version 4.0
    lahman45ID, ID used in Lahman database version 4.5
    retroID, ID used by retrosheet
    holtzID, ID used by Sean Holtz's Baseball Almanac
    bbrefID, ID used by Baseball Reference website
    deathDate,Date of Death
    birthDate,Date of Birth
    yearID, Year
    stint, player's stint (order of appearances within a season)
    teamID, Team
    lgID, League
    G, Games
    G_batting, Game as batter
    AB, At Bats
    R, Runs
    H, Hits
    2B, Doubles
    3B, Triples
    HR, Homeruns
    RBI, Runs Batted In
    SB, Stolen Bases
    CS, Caught Stealing
    BB, Base on Balls
    SO, Strikeouts
    IBB, Intentional walks
    HBP, Hit by pitch
    SH, Sacrifice hits
    SF, Sacrifice flies
    GIDP, Grounded into double plays
    G_Old, Old version of games (deprecated)
    salary, Salary

## Narrow down the input variables

You might also want to consider variable to group by, or how some variables can be made valuable through your manipulation. The features not of interest were removed.

### Group By

    managerID, An ID for individuals who served as managers
    teamID, Team
    lgID, League

### Interesting, but problematic or more work

    hofID, An ID for individuals who are in teh baseball Hall of Fame
    bats, Player's batting hand (left, right, or both)
    birthYear, Year player was born
    birthMonth, Month player was born

### Intuitive Input Variables:

    yearID, Year
    G, Games
    AB, At Bats
    R, Runs
    H, Hits
    2B, Doubles
    3B, Triples
    HR, Homeruns
    RBI, Runs Batted In
    BB, Base on Balls
    SO, Strikeouts
    IBB, Intentional walks
    weight, Player's weight in pounds
    height, Player's height in inches

# Output Variable:

    salary, Salary

Define your array of features and response variable and load the data

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import feature_selection, linear_model

response = ['salary']
features = ['weight', 'height', 'yearID', 'R', 'X2B', 'X3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO']

# Create a new dataframe
base = pd.read_csv('https://raw.github.com/ga-students/DS_HK_1/gh-pages/data/class/baseballRegressionData/baseball.csv')

```

## Investigate what type of players you're dealing with

Is it possible to filter out the pitcher who might be more vabluable for their pitching skills than hitting? E.g. you can ask for `Balls Thrown (BT) > 0` to capture all the pitchers

```python
  base[base['BT'] > 0]
```

But there's no `BT` or any other pitching statistics! You've just discovered that you're dealing with a subset of the original dataset.

To sort the players by `Batting Average` and return the 10 best seasonal performances in the history of the game!

```python
# Select numerical feature
base_reduced = base[features + response]

# Deal with NA
base_drop = base_reduced.dropna()

# Response
salary = base_drop['salary'].values

# Input
base_input = base_drop[features].values

# Run feature analysis
features_set = feature_selection.univariate_selection.f_regression(base_input, salary)
```

```python
"""
F-score Results: array([  720.19551844,   159.83314039,  2587.27918777,  1261.17935071,
                          1084.86319699,    33.28502517,  1949.84037943,  1564.51125799,
                            82.15550475,    16.79825842,  1454.01703771,   897.86923661])

# p-value results: array([  7.31863781e-156,   1.70195645e-036,   0.00000000e+000,
                                 7.21130290e-268,   1.09046286e-231,   8.07781495e-009,
                                 0.00000000e+000,   0.00000000e+000,   1.37210310e-019,
                                 4.17367975e-005,   4.33920494e-307,   5.61159565e-193]))

"""
```
```python
fp = zip(features, features_set[1])

sorted(fp, key=lambda p: p[1])
```

Based on the following results we know 'yearID','HR','RBI','BB','R', and 'X2B' are significant features. We can use these four features for out model. Worth noting none of these are surprising: Home Runs, Runs Batted
In and Runs scored all are hugely important in helping a baseball club win games, thus a player with
more of these statistics seems reasonably like to earn a higher salary. Additionally, as Business
Insider show demonstrates
(http://www.businessinsider.com/chart-of-the-day-major-league-baseball-salaries-since-1970-2011-1)
The average salary in Major League Baseball has grown exponentially over the past 40 years as TV deals
and sponsorship agreements have driven club revenue, and athletes have gains a more prominent role
in American society.


```python
[('yearID', 0.0),
 ('HR', 0.0),
 ('RBI', 0.0),
 ('BB', 4.3392049377349969e-307),
 ('R', 7.2113028958220647e-268),
 ('X2B', 1.0904628564774478e-231),
 ('SO', 5.6115956481581205e-193),
 ('weight', 7.3186378104902299e-156),
 ('height', 1.701956448805751e-36),
 ('SB', 1.372103097111745e-19),
 ('X3B', 8.0778149508959948e-09),
 ('CS', 4.1736797544881667e-05)]

```

```python


features_subset = ['yearID','HR','RBI','BB','R','X2B']

# Seperate significant features
X = base_drop[features_subset].values

# Use ridge regression model
ridge = linear_model.Ridge()
salaryFit = ridge.fit(X, salary)

# Predict salary based on fit of features
salaryPredict = salaryFit.predict(X)

# Check score of the regression fit
salaryFit.score(X, salary)

# Result: 0.20799776836490136 This terrible.
```

** Switch to the Data Exploration and Dignostics on the Wiki before returning here for deeper investigation into the dataset **

## Average Scores

Some of the most important baseball statistics are missing! Calculate these ratios yourself, for example:

```python
from __future__ import division

base['BA'] = base['H']/base['AB']

base.sort('BA', ascending=False).head(10)
```

## Looking at Team Budgets

```python
grouped = base.groupby('teamID')['salary'].mean()
grouped.order(ascending=False)

# Sanity Check
base['salary'].describe()
grouped.plot(kind='bar', colormap='rainbow')
plt.show()

zscore = lambda x: (x - x.mean()) / x.std()

### Looking at player salary per team budget
g = base.groupby('teamID')['salary']
z = g.apply(zscore)

base['budget_z'] = z
```
If we inspect the results, we'll find that the results aren't in line with what
we expected. Some teams have relatively low bugdets (e.g. Miami Marlins) but rank
very highly in the graph. We forgot to account for the exponential growth in
budgets over time! As the Miami Marlins are a relatively new team, they didn't
compete at a time when salaries were relatively lower.

To group and plot by two variables involves `unstacking` the group

```python

grouped = base.groupby(['yearID','teamID'])['salary'].mean()
grouped.unstack().plot(colormap='rainbow')
plt.show()

zscore = lambda x: (x - x.mean()) / x.std()
g = grouped = base.groupby(['yearID','teamID'])['salary']

z = g.apply(zscore)
```

Now you are comparing a player's salary against the other players on _his team_
for _the year_ in which the salary was recorded. Awesome!


## Resources

### Technical Tools
* [GroupBy-fu: improvements in grouping and aggregating data in pandas](http://wesmckinney.com/blog/?p=125)


