

# read data
college <- read.csv("http://www-bcf.usc.edu/~gareth/ISL/College.csv")
colnames(college)
head(college)
?row.names
row.names(college)

# rename rows with the column named x in dataframe college
head(college)
row.names(college)

row.names(college)<- college$x

# look at first column
head(college$x)

#delete the redundatn first column
college$x = NULL

#
summary(college)

#
pairs(college[,1:3])

#
colnames(college)

#
hist(college$Apps)
hist(college$Books)
