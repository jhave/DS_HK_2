#
# rpubs.com/slygent/statlearn
#
2+2
sum (2,3,4000,pi)
x = c(1,8,7,15)
x
y=c(20,5,6,4)
y+x
y^2
ls()
rm(y)
?matrix
matrix(data=c(1,2,3,4),nrow=2,ncol=2)
matrix(data=c(1,2,3,4),2,2)
set.seed(3)
y=rnorm(100)
y
mean(y)
var(y)
x=rnorm(100)
y=rnorm(100)
plot(x,y)

# seq and outer
x= seq (-pi,pi,length=50) # from -pi to pi in 50 steps
head(x)
y=x
head(y)
f=outer(x,y,function(x,y)cos(y)/1+x^2)#combines every number in x with every number in y to create a 50 x 50 grid
contour(x,y,f)

# matrix
A=matrix(1:16,4,4)
A
A[1,]
A[2,3]
A[c(1,3),c(2,4)]

#display some numbers
3:7

# read data
auto <- read.csv("http://www-bcf.usc.edu/~gareth/ISL/Auto.csv")
colnames(auto)
head(auto)
?row.names
row.names(auto)=c()

# use i