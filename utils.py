import numpy as np

def rand(range):
    num = round((np.random.random()*(range[1] - range[0]))) + range[0]
    return num

def rand_not(range, not_num):
    ''' 
    takes tuple range (lower, upper)
    and not which is excluded
    '''
    num = not_num[0]
    while (num in not_num):
        num = round((np.random.random()*(range[1] - range[0]))) + range[0]
    return num