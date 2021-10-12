from math import sqrt

# Euclidian distance
def euclidian(start, end):
    return sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)

# Manhattan distance
def manhattan(start, end):
    return abs(start[0]-end[0]) + abs(start[1]-end[1])

# Chebyshev distance
def chebyshev(start, end):
    return max(abs(start[0]-end[0]), abs(start[1]-end[1]))

# Euclidean and Manhattan
def manhattan_three(start, end):
    return manhattan(start, end) * 3

def chebyshev_manhattan(start, end):
    return manhattan(start, end) + chebyshev(start, end)

def chebyshev_euclidian(start, end):
    return euclidian(start, end) + chebyshev(start, end)

def manhattan_euclidian(start, end):
    return euclidian(start, end) + chebyshev(start, end)