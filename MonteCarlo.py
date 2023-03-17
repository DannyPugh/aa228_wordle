import numpy as np
from numpy import inf, sqrt, log
from random import choices
#import display as dsp

class MDP:
    def __init__(self, S = [], A= [], T= [], R= [], y = 0, U = [], TR = sum):
        self.S  = S     # state space (list of all possible dictionary words x all possible color combinations  3456780)
        self.A  = A     # action space (list all possible dictionary "guesses"/words)
        self.T  = T     # transition function
        self.R  = R     # reward function
        self.y  = y     # discount factor
        self.U  = U     # value function 
        self.TR = TR    # sample transition and reward (function)

class MonteCarloTreeSearch:
    def __init__(self, N = {}, Q = {}, d = 0, m = 0, c = 0, U = {}, P = MDP()):
        self.N  = N     # visit counts (start as empty dictionary)
        self.Q  = Q     # action value estimates (start as empty dictionary)
        self.d  = d     # depth
        self.m  = m     # number of simulations
        self.c  = c     # exploration constant
        self.U  = U     # value function estimate (initialize to zero???)
        self.P  = P     # Problem initialize to MDP of problem

    def bonus(self, Nsa, Ns):
        if Nsa == 0:
            return inf
        else:
            return sqrt(log(Ns)/Nsa)

    def explore(self, s):
        Ns = np.sum(self.N[(s,a)] for a in self.P.A)
        UCB_list = []
        for a in self.P.A: 
            UCB_list.append(self.Q[s, a] + self.c*self.bonus(self.N[(s,a)], Ns))
        return self.P.A[np.argmax(np.asarray(UCB_list))]

    def simulate(self, s, d):
        if self.d <= 0:
            return self.U(s)
        if not((s, self.P.A[0]) in self.N):
            # initialize all Ns and Qs
            for a in self.P.A:
                self.N[(s,a)] = 0
                self.Q[(s,a)] = 0.0
            return self.U[s]
        a = self.explore(s)
        s_prime, r  = self.P.TR(s,a)
        #terminate on end goal and lower bound
        # if o == 'GGGGG':
        #     d = 0
        # elif o == 'ggggg':
        #     d = 0
        q = r + self.P.y*self.simulate(s_prime, d-1)
        self.N[(s,a)] += 1
        self.Q[(s,a)] += (q - self.Q[(s,a)])/self.N[(s,a)]
        return q

    def monte_carlo(self): # s is the current state
        for i, s in enumerate(choices(self.P.S, k = self.m)):
            self.simulate(s, self.d)
            dsp.status_hub(i,self.m,s,max(self.Q, key = self.Q.get)[1])
        return max(self.Q, key = self.Q.get) # return the action that maximizes Q