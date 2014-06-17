library(MASS)
library(ISLR)
# fix(Boston)
names(Boston)

bostonlm <- lm(medv~lstat,data=Boston) # median home value vs low economic status
plot(Boston$lstat, Boston$medv)
abline(bostonlm)

lm(formula = medv ~ lstat + age, data = Boston)


#
#Carry out linear regression of mpg against horsepower. Use summary to print the results.
# read data
auto <- read.csv("http://www-bcf.usc.edu/~gareth/ISL/Auto.csv")
head(auto)
# visualize the effect of mpg on predicting horsepower
summary (lm(mpg ~ horsepower, data= auto))
Autolm <-lm(mpg~horsepower,data=auto)
plot(auto$mpg,auto$horsepower)
abline(autolm)


# predict

predict (lm(mpg ~ horsepower, data= Auto), newdata=data.frame(horsepower=98))
plot (Auto$horsepower,Auto$mpg)
Autolm <-lm(mpg~horsepower,data=Auto)
abline(Autolm)
