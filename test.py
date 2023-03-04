import Q_Learning as ql
import pandas as pd
import numpy as np

def save_to_csv(filename, data, fmt_ = '%e4'):
    """
    Save a NumPy array to a CSV file.

    Parameters:
    filename (str): Name of the output file.
    data (np.ndarray): NumPy array to be saved.

    Returns:
    None
    """
    np.savetxt(filename, data, delimiter=",", fmt = fmt_)

data_set = 'large'

if data_set == 'small':
    y = 0.95    # discount
    alpha = 0.5 # learning rate
    n = 10000   # iterations

    df = pd.read_csv('data/small.csv')
    s = 10*10   # number of states
    a = 4       # number of actions

elif data_set == 'medium':
    y = 1    # discount
    alpha = 0.75 # learning rate
    n = 100000   # iterations

    df = pd.read_csv('data/medium.csv')
    s = 500*100   # number of states
    a = 7      # number of actions

elif data_set == 'large':
    y = 0.95    # discount
    alpha = 0.75 # learning rate
    n = 100000   # iterations

    df = pd.read_csv('data/large.csv')
    s = 312020   # number of states
    a = 9      # number of actions


env = ql.Environment(df, s, a)

agent = ql.Q_Learning(env, y, alpha)

try:
    count = 0
    while True:
        print(f'starting new iteration {count}')
        for i in range(n):
            s,a,r,sp = np.asarray(env.sample_next())
            agent.update(s-1,a-1,r,sp-1)   
        new_Q = agent.Q
        policy = (agent.get_policy()+1).round()
        count += 1
finally:
    print("saving results to file")
    save_to_csv(f'results/{data_set}_Q.csv', new_Q)
    save_to_csv(f'results/{data_set}.policy', policy, '%d')
    agent.visualize_Q()
