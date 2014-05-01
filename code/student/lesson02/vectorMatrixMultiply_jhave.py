"""Write 2 more functions 
vectorMatrix multiplication 
and 
matrix multiplication. 

No numpy/scipy! 
Do this with pure python. 
Use triple quotes/doc quotes to explain the properties 
expected for a matrix in these functions:"""

matrix = [ [1, 2, 3, 4], 
           [5, 6, 7, 8],
           [9, 0, 1, 2] ]
vector = [1 ,2, 3]

def vectorMatrixMultiply(vect,matr):
           
    # optimal goal form of TRANSPOSE return [ [row[i] for row in vect] for i in range(len(matr[0]))]

    """ TEST #1
    for row in vect:
        for col in matr:
            print row * col
            """
    
    """ TEST #2
    for iv in range(len(vect)):
        for im in range(len(matr)):
            print "iv:", iv, " vect[iv]: ", vect[iv], "  vect[im]: ", vect[im],"  im:", im, "  matr[im][iv]: ", matr[im][iv]
            """
    
    """ TEST #3
    for im in range(len(matr[0])):
        for iv in range(len(vect)):
            print "im:", im ,  "iv:", iv ,"  vect[iv]: ", vect[iv], "  matr[im][iv]: ", matr[iv][im],  "  matr[im][iv] * vect[im]: ", matr[iv][im] * vect[iv]
          """
    """ TEST 4
     # initialize multi dimensional array
    newlist=[[0 for x in xrange(len(vect))] for x in xrange(len(matr[0]))]

    for im in range(len(matr[0])):
        for iv in range(len(vect)):
             newlist[iv] += matr[iv][im] * vect[iv]
            #  WRONG MATH: this returns the product    newlist[im][iv] = matr[iv][im] * vect[iv]

    return  newlist      
    """

    """ sum the product of row j in vect with value in col i """
    return [sum(matr[i][j]*vect[j] for j in range(len(vect))) for i in range(len(matr))]     
                        
# call function        
print vectorMatrixMultiply(vector,matrix)