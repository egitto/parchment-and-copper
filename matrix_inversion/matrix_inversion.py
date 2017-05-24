from copy import deepcopy
from fractions import Fraction as Fract

def invert(matrix):
    """Inverts the matrix. Requires python's Fract library.

    If matrix is singular, prints 'Inversion impossible' and returns nothing.
    """
    matrix = as_Fractions(matrix)
    accum = deepcopy(matrix)
    size = len(matrix)
    inverse_accum = identity_matrix(size)
    row = 0 # row being processed
    singular = False
    loopcount = 0
    # this while loop makes the matrix triangular
    while row < size:
        loopcount += 1
        # make matrix[row][row] = 1 if it doesn't already
        # eliminate all entries below matrix[row][row]
        # then accum will be triangular upper
        try:
            row_op = create_row_operation(size,row,row,Fract(1,accum[row][row]))
        except(ZeroDivisionError):
            # currently singular, attempt fixing
            # if it can't be fixed, throw an exception
            # and the original matrix will be modified
            # print("Singular matrix found:")
            # print(accum)
            # print("Attempting fix by swapping for a later row")
            fix = -1
            for i in range(row+1, size):
                # print("Testing row "+str(i)+" out of "+str(size))
                if accum[i][row] != 0:
                    # print("Row "+str(i)+" will fix")
                    fix = i
                    break
            if fix == -1:
                print('Inversion impossible'); return
            row_op = rowSwap(size,fix,row)
        ("Matrix operation: "+ str(row_op))
        # print("Accumulated: " + str(accum))
        accum = matrix_multiply(row_op,accum)
        # print("After operation: " + str(accum))
        inverse_accum = matrix_multiply(row_op,inverse_accum)
        if accum[row][row] == 1:
            # print("Checking "+str(column(accum,row)[(row+1):])+" against "+str([0]*(size-row-1)))
            if column(accum,row)[(row+1):] == [0]*(size-row-1):
                # print("Row "+str(row)+" finished, progressing")
                row += 1
            else: # need to make the zeroes below the cursor
                for i in range(row+1, size):
                    # Need to nullify below accum[i][row], to maintain invariant
                    row_op = create_row_operation(size,row,i,-accum[i][row])
                    # print("Matrix operation: "+ str(row_op))
                    # print("Accumulated: " + str(accum))
                    accum = matrix_multiply(row_op,accum)
                    # print("After operation: " + str(accum))
                    inverse_accum = matrix_multiply(row_op,inverse_accum)
                # print("Column below "+str(row)+","+str(row)+" should be zeroes:")
                # print(accum)
    # this while loop performs backsubstitution
    row = size-1
    while row >= 0:
          # cursor starts at bottom-right, zeros out everything above
          # then moves up 1, left 1, repeats
          # print("Checking "+str(column(accum,row)[:row])+" against "+str([0]*(row)))
          if column(accum,row)[0:row] == [0]*(row):
                # print("Row "+str(row)+" finished, progressing")
                row -= 1
          else:
                for i in range(0,row):
                    row_op = create_row_operation(size,row,i,-accum[i][row])
                    # print("Matrix operation: "+ str(row_op))
                    # print("Accumulated: " + str(accum))
                    accum = matrix_multiply(row_op,accum)
                    # print("After operation: " + str(accum))
                    inverse_accum = matrix_multiply(row_op,inverse_accum)
    # print("Accumulated: should be identity matrix")
    # print(accum)
    # print("Accumulated matrix operations (aka inverse):")
    # print(inverse_accum)
    return inverse_accum

def identity_matrix(n):
    """Returns the identity matrix of size n
    """
    acc = []
    for i in range(n):
        acc += [[0]*n]
        acc[i][i] = 1
    return acc

def create_row_operation(size,origin,dest,quantity):
    """Returns a matrix that performs the following actions when multiplied against a sizeXsize matrix:
    if origin = dest, multiplies the row by quantity
    if origin != dest, adds (origin row * quantity) to dest row
    """
    a = identity_matrix(size)
    if origin == dest:
        a[origin][origin] = quantity
    else:
        a[dest][origin] = quantity
    return a

def matrix_multiply(matrix_1,matrix_2):
    """Returns matrix_1*matrix_2, where both arguments are matricies of compatible length
    """
    assert len(matrix_1[0]) == len(matrix_2), 'incompatible matrices'
    acc = []
    for i in range(len(matrix_1)):
        # for each new row
        acc += [[]]
        for j in range(len(matrix_2[0])):
            acc[i] += [sum(vector_multiply(matrix_1[i],column(matrix_2,j)))]
    assert type(acc) == list, 'matrix_multiply output not list'
    assert type(acc[0]) == list, 'matrix_multiply output not matrix'
    return acc

def vector_multiply(v1,v2):
    assert len(v1) == len(v2), 'vectors incorrect lengths'
    return [v1[i]*v2[i] for i in range(len(v1))]

def column(matrix, i):
    return [row[i] for row in matrix]

def as_Fractions(matrix):
    return [[Fract(j) for j in i] for i in matrix]

def as_floats(matrix):
    return [[float(j) for j in i] for i in matrix]