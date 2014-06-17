Advertising = read.csv("http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv")
head(Advertising, n=3)

#
library(class)
knn(k=9)


# lm linear model ( OUTPUT ~ predictors + predictors....)
summary (lm(Sales ~ TV + Radio + Newspaper, data= Advertising))

# visualize the effect of TV on Radio with TV:Radio
summary (lm(Sales ~ TV + Radio + TV:Radio, data= Advertising))


# visualize the effect of TV on Radio with TV:Radio
summary (lm(Sales ~ TV + Radio + I(TV^2), data= Advertising))
