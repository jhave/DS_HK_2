'''
Code for GA Data Science, Lesson 6 "Polynomial Regression" by Freda, Monday 19 May 2014
Predicting City Miles Per Gallon of cars
Dataset here: 
https://gist.githubusercontent.com/tijptjik/3746ac7c1f0ec6953ed7/raw/6561674a1c1edff3b7f78fcce326df5c72bf402e/cars93.csv
'''

from pandas import read_csv, DataFrame
from numpy import mean
from sklearn import linear_model, feature_selection
# so far did not use import matplotlib.pyplot as plt


car = read_csv('cars_complex.csv')

# clean up strings in the data
car_x = car._get_numeric_data()
car_x = car_x.fillna(car_x.mean())

car_y = car_x['MPG.city']

# drop the y from the input variables
car_x = car_x.drop(['MPG.highway','MPG.city'], 1)

# No need to put univariate feature selection. 
f = feature_selection.f_regression(car_x, car_y)

# show F scores in np array
fscore = zip(car_x.columns.values,f[0])

fscorePD = DataFrame(fscore)
fscorePD.columns = ['Car_x', 'F score']

"""
In [43]: fscorePD
Out[43]:
                 Car_x     F score
0            Min.Price   57.686448
1                Price   49.758834
2            Max.Price   39.017977
3           EngineSize   92.506400
4           Horsepower   75.191648
5                  RPM   13.814772
6         Rev.per.mile   85.430767
7   Fuel.tank.capacity  177.598088
8           Passengers   19.138664
9               Length   72.632116
10           Wheelbase   72.973600
11               Width   98.256009
12         Turn.circle   72.690899
13      Rear.seat.room   15.399246
14        Luggage.room   24.722024
15              Weight  223.751044

[16 rows x 2 columns]
"""


# show p values in np array
# Since p values are derived from F scores, the following code concerning p values is just a way to check my work. 
pvalue = zip(car_x.columns.values, f[1])

pvaluePD = DataFrame(pvalue)
pvaluePD.columns = ['Car_x','p value']

"""
In [46]: pvaluePD
Out[46]:
                 Car_x       p value
0            Min.Price  2.616835e-11
1                Price  3.308302e-10
2            Max.Price  1.322911e-08
3           EngineSize  1.605973e-15
4           Horsepower  1.536840e-13
5                  RPM  3.481301e-04
6         Rev.per.mile  9.797507e-15
7   Fuel.tank.capacity  4.177320e-23
8           Passengers  3.231623e-05
9               Length  3.142612e-13
10           Wheelbase  2.854669e-13
11               Width  3.890182e-16
12         Turn.circle  3.091008e-13
13      Rear.seat.room  1.688050e-04
14        Luggage.room  3.101475e-06
15              Weight  2.967048e-26

[16 rows x 2 columns]
"""

# For easy viewing, sort in descending order
fscorePD.sort(['F score'], ascending=False, inplace=True)

"""
In [52]: fscorePD
Out[52]:
                 Car_x     F score
15              Weight  223.751044
7   Fuel.tank.capacity  177.598088
11               Width   98.256009
3           EngineSize   92.506400
6         Rev.per.mile   85.430767
4           Horsepower   75.191648
10           Wheelbase   72.973600
12         Turn.circle   72.690899
9               Length   72.632116
0            Min.Price   57.686448
1                Price   49.758834
2            Max.Price   39.017977
14        Luggage.room   24.722024
8           Passengers   19.138664
13      Rear.seat.room   15.399246
5                  RPM   13.814772

[16 rows x 2 columns]

"""

pvaluePD.sort(['p value'], ascending=False, inplace=True)

"""
In [54]: pvaluePD
Out[54]:
                 Car_x       p value
5                  RPM  3.481301e-04
13      Rear.seat.room  1.688050e-04
8           Passengers  3.231623e-05
14        Luggage.room  3.101475e-06
2            Max.Price  1.322911e-08
1                Price  3.308302e-10
0            Min.Price  2.616835e-11
9               Length  3.142612e-13
12         Turn.circle  3.091008e-13
10           Wheelbase  2.854669e-13
4           Horsepower  1.536840e-13
6         Rev.per.mile  9.797507e-15
3           EngineSize  1.605973e-15
11               Width  3.890182e-16
7   Fuel.tank.capacity  4.177320e-23
15              Weight  2.967048e-26

[16 rows x 2 columns]

"""



