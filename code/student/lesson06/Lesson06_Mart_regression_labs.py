import pandas as pd
import matplotlib.pyplot as plt
from numpy import log, exp, mean
from sklearn import linear_model, feature_selection

DATA_DIR = '../../../data/'

def SSE(pred, resp):
 	return mean((pred - resp) ** 2)

"""
Find the best fitting model to predict breaking distance for car speed
"""

stop = pd.read_csv(DATA_DIR + 'cars.csv')

# Convert the data into appropriate data structure
# first parameter of FIT called below has to be a MATRIX
# so the syntax of the following for is for only when there is a single feature such as in this case
speed = [[x] for x in stop['speed']]
dist = stop['dist'].values

# FIRST STEP TO DO 
#Inspect the distribution to visually check for linearity and normality
plt.scatter(speed, dist, c='b', marker='o')
plt.show()

# Attempt 1 : Simple Linear Model
regr = linear_model.LinearRegression()
regr.fit(speed, dist)

print "\nSpeed | Distance"
print "SSE : %0.4f" % (SSE(regr.predict(speed), dist)) # SSE : 227.0704
print "R2 : %0.4f" % (regr.score(speed, dist)) # R2 : 0.6511

plt.scatter(speed, dist, c='b', marker='o')
plt.plot(speed, regr.predict(speed), color='green')
plt.show()

# Attempt 2 : Lasso Regression Model with 3nd order polynominal 
# reduces some variables to 0, so smoothing irrelevants
stop['speed_squared'] = stop['speed'] ** 2
speed_squared = stop[['speed','speed_squared']].values

lasso = linear_model.Lasso()
lasso.fit(speed_squared, dist)

print "\nSpeed | Distance"
print "SSE : %0.4f" % (SSE(lasso.predict(speed_squared), dist)) # SSE : SSE : 217.3360
print "R2 : %0.4f" % (lasso.score(speed_squared, dist)) # R2 : 0.6660

plt.scatter(speed, dist, c='b', marker='o')
plt.plot(speed, lasso.predict(speed_squared), color='green')
plt.show()

# Attempt 3 : Ridge Regression Model with 2nd order polynominal 
# will not reduce outliers to zero, smooths...
ridge = linear_model.Ridge()
ridge.fit(speed_squared, dist)

print "\nSpeed | Distance"
print "SSE : %0.4f" % (SSE(ridge.predict(speed_squared), dist)) # SSE : 216.4946
print "R2 : %0.4f" % (ridge.score(speed_squared, dist)) # R2 : 0.6673

plt.scatter(speed, dist, c='b', marker='o')
plt.plot(speed, ridge.predict(speed_squared), color='green')
plt.show()

# Attempt 4 : Ridge Regression Model with 3nd order polynominal 
stop['speed_boxed'] = stop['speed'] ** 3
speed_boxed = stop[['speed','speed_squared','speed_boxed']].values

ridge = linear_model.Ridge()
ridge.fit(speed_boxed, dist)

print "\nSpeed | Distance"
print "SSE : %0.4f" % (SSE(ridge.predict(speed_boxed), dist)) # SSE : SSE : 212.8165
print "R2 : %0.4f" % (ridge.score(speed_boxed, dist)) # R2 : 0.6730

plt.scatter(speed, dist, c='b', marker='o')
plt.plot(speed, ridge.predict(speed_boxed), color='green')
plt.show()

# Attempt 5 : Ridge Regression Model with 3nd order polynominal 

# alpha, setting the alpha,
for a in [0.1,0.5,1,5,10]:

	# feed in the alphas
	ridge = linear_model.Ridge(alpha=a)
	ridge.fit(speed_boxed, dist)

	print "\nSpeed | Distance @ " + str(a)
	print "SSE : %0.4f" % (SSE(ridge.predict(speed_boxed), dist)) # SSE : SSE : 212.8165
	print "R2 : %0.4f" % (ridge.score(speed_boxed, dist)) # R2 : 0.6730


# Attempt 6 : Ridge Regression Model with 3nd order polynominal 

ridge = linear_model.Ridge()
ridge.fit(speed_boxed, dist)

	print "\nSpeed | Distance @ " + str(a)
	print "SSE : %0.4f" % (SSE(ridge.predict(speed_boxed), dist)) # SSE : SSE : 212.8165
	print "R2 : %0.4f" % (ridge.score(speed_boxed, dist)) # R2 : 0.6730


"""
Find the best fitting model to predict mileage for gallon
"""

cars = pd.read_csv('cars_complex.csv')

# internal method to get rid of columns with string info
cars_input = cars._get_numeric_data()
# drop all cars with missing values (rough solution)
cars_input = cars_input.dropna(axis=0)

#store response variable
mpg = cars_input['MPG.city']

# get rid of response variable
cars_input = cars_input.drop(['MPG.highway','MPG.city'],1)

# feature_selection module from scikitlearn can select features...
fp_value = feature_selection.univariate_selection.f_regression(cars_input, mpg)

# increase legibility by using ZIP to make one list out of 2
# cars_input.columns.values is the NAMEs of the columns
# fp_value[1] is the p-values
p_value = zip(cars_input.columns.values,fp_value[1])
# sort by the fp_value
sorted(p_value,key=lambda x: x[1])

#   PRINT>>>>
#pValuePD = pd.DataFrame(p_value)
#pValuePD.columns = ['Car_x', 'F score']

#
"""  CTRL b

 NEXT STEP...
after manual step CROSS-VALIDATE
drop Weight and repeat f

consdierations
how much can i use?
how costly is it to collect?
"""

