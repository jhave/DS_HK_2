#! /usr/bin/env python

def main():
    import pandas as pd
    from sklearn import linear_model, metrics
    from sklearn.neighbors import KNeighborsClassifier
    b2011 = pd.read_csv('baseball_training_2011.csv')
    b2012 = pd.read_csv('baseball_test_2012.csv')
    #
    """
LG League
G Games
AB At Bats
R Runs
H Hits
X2B Doubles
X3B Triples
HR Homeruns
RBI Runs Batted In
SB Stolen Bases
CS Caught stealing              - removed
BB Base on Balls
SO Strikeouts                   - removed
IBB Intentional walks
HBP Hit by pitch
SH Sacrifices
SF Sacrifice flies
GIDP Grounded into double plays - removed

    """
    train_X = b2011[['G', 'AB', 'R', 'H', 'X2B', 'X3B', 'HR', 'RBI', 'SB',  'BB',  'IBB', 'HBP', 'SH', 'SF']].values
    train_y = b2011['salary'].values
    #
    test_X = b2012[['G', 'AB', 'R', 'H', 'X2B', 'X3B', 'HR', 'RBI', 'SB',  'BB',  'IBB', 'HBP', 'SH', 'SF']].values
    b2012_csv = b2012[['playerID','yearID', 'salary']]
    #
    lm = linear_model.Ridge()
    lm.fit(train_X, train_y)
    #
    #kn = KNeighborsClassifier(3)
    #kn.fit(train_X,train_y)
    #
    # Checking performance, roughly .19
    #print 'R-Squared:',lm.score(train_X, train_y)
    print 'R-Squared:',lm.score(train_X, train_y)
    # Checking MSE, roughly terrible
    #print 'MSE:',metrics.mean_squared_error(lm.predict(train_X), train_y)
    
    # documentation says: sklearn.metrics.mean_squared_error(y_true, y_pred) 
    # QUESTION: Are the variables reversed?
    print 'MSE:',metrics.mean_squared_error(lm.predict(train_X),train_y)
    #
    # Outputting to a csv file
    print "Outputting submission file as 'submission.csv'"
    b2012_csv['predicted'] = lm.predict(test_X)
    #b2012_csv['predicted'] = kn.predict(test_X)
    b2012_csv.to_csv('Jhave_submission1(based on benchmark).csv')


    """
OUTPUT using linear_model.Ridge    and same variables as given
R-Squared: 0.191236646455
MSE: 1.70429254467e+13
Outputting submission file as 'submission.csv'
[Finished in 47.1s]

OUTPUT using linear_model.Ridge  
R-Squared: 0.166487207289
MSE: 1.75644659501e+13
Outputting submission file as 'submission.csv'
[Finished in 1.2s]

OUTPUT using KNeighborsClassifier(3)   and same variables as given
R-Squared: 0.310478654592
MSE: 2.26515594803e+13
Outputting submission file as 'submission.csv'
[Finished in 1.4s]

OUTPUT use KNeighborsClassifier(3)
R-Squared: 0.304010349288
MSE: 2.32753191824e+13
Outputting submission file as 'submission.csv'
[Finished in 1.4s]

i think i made it worse!

    """

if __name__ == "__main__":
    main()
