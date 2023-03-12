import numpy as np

def rand_not(range, not_num):
    ''' 
    takes tuple range (lower, upper)
    and not which is excluded
    '''
    num = not_num
    while (num == not_num):
        num = round((np.random.random()*(range[1] - range[0]))) + range[0]
    return num


for i in range(20):
    print(rand_not((0,4),3))



    
