import Q_Learning as ql
import pandas as pd
import numpy as np


data_set = 'small'

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


Q = np.asarray(pd.read_csv(f'results/{data_set}_Q.csv'))
env = ql.Environment(df, s, a)

agent = ql.Q_Learning(env, y, alpha)
agent.Q = Q

agent.visualize_Q()