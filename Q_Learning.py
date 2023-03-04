import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, df, states, actions):
        self.df = df
        self.states = states
        self.actions = actions
        self.index = -1

    def randomize(self):
        self.df = self.df.sample(frac=1)

    def sample_next(self):
        self.index += 1
        if self.index >= len(self.df):
            self.index = 0
        return self.df.loc[self.index]
        



class Incremental_Estimation:
    def __init__(self, u, a, m):
        self.u = u
        self.a = a
        self.m = m

    def update(self, x):
        self.m += 1
        self.u += self.a(self.m) * (x - self.u) 
        return self

class Q_Learning:
    def __init__(self, env, y, alpha):
        self.y = y
        self.alpha = alpha

        self.S = env.states
        self.A = env.actions
        self.Q = np.zeros([self.S,self.A])

    def update(self, s, a, r, sp):
        self.Q[s,a] += self.alpha*(r + self.y*np.max(self.Q[sp,:]) - self.Q[s,a])

    def visualize_Q(self, rotate = False):
        fig, ax = plt.subplots()
        if rotate == False:
            ax.imshow(self.Q)
        else:
            ax.imshow(self.Q.T)
        plt.show()

    def get_policy(self):
        return np.argmax(self.Q,1)

