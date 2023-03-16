import numpy as np
from numpy import inf, sqrt, log



class MDP:
    def __init__(self, S, A, T, R, y, U, TR):
        self.S  = S     # state space
        self.A  = A     # action space
        self.T  = T     # transition function
        self.R  = R     # reward function
        self.y  = y     # discount factor
        self.U  = U     # value function
        self.TR = TR    # sample transition and reward

class MonteCarloTreeSearch:
    def __init__(self, N, Q, d, m, c, U, P = MDP()):
        self.N  = N     # visit counts (dictionary)
        self.Q  = Q     # action value estimates
        self.d  = d     # depth
        self.m  = m     # number of simulations
        self.c  = c     # exploration constant
        self.U  = U     # value function estimate
        self.P = P      # Problem

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
        return np.argmax(np.asarray(UCB_list))

    def simulate(self, s, d):
        if self.d <= 0:
            return self.U(s)
        if self.N.has_key(s, self.P.A[0]):
            for a in self.P.A:
                self.N[(s,a)] = 0
                self.Q[(s,a)] = 0.0
            return self.U(s)
        a = self.explore(s)
        s_prime, r = self.P.TR(s,a)
        q = r + self.P.y*self.simulate(s_prime, self.d-1)
        self.N[(s,a)] += 1
        self.Q[(s,a)] += (q - self.Q[(s,a)])/self.N[(s,a)]
        return q


    def MonteCarloMain(self, s): # s is the current state
        for _ in range(self.m):
            self.simulate(s, self.d)
        return np.argmax(self.Q[s, :]) # return the action that maximizes Q