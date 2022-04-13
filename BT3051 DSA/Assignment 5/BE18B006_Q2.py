import matplotlib.pyplot as plt
from numpy import random
# no other libraries are allowed

def func(x):
    return 1/x

def Estimated_area_under_curve(func, lower_limit, higher_limit):
    """
    Estimate the area under the curve for a given function using the method discussed in the class using random numbers.
    Assume the input function to be monotonic.
    """
    area = 0
    """ Add your code here """
    curve, box, l, iternum = 0, 0, 100000, 10
    for i in range(iternum):
        x_sample, y_sample = random.uniform(lower_limit, higher_limit, l), random.uniform(0, max(func(lower_limit), func(higher_limit)), l)
        for j in range(l):
            if y_sample[j] > func(x_sample[j]):
                box += 1
            else:
                curve += 1
                box += 1
        area += (curve / box) * (higher_limit - lower_limit) * max(func(lower_limit), func(higher_limit))
    area = area / iternum
    return area

Estimated_area = Estimated_area_under_curve(func, 1/2, 2)
estimated_e = 0
# Find the area under the curve analytically. Equating the analytical expression and with the estimated value, find the value of the irrational number e. Hint, use log to the base 2.
""" Add your code here """
# Analytical solution: area = 2 ln (2)
# e = 2 ** (2 / area)

estimated_e = 2 ** (2 / Estimated_area)
print("e = ", str(estimated_e), sep='')