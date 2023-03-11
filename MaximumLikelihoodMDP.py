from socket import IPV6_RTHDR_TYPE_0
import numpy as np
from math import inf

class MaximumLikelihoodMDP:
    def __init__(self, S, A, N, p, y, U):
        self.S  = S     # state space
        self.A  = A     # action space
        self.N  = N     # transition        [state, action, state']
        self.p  = p     # reward
        self.y  = y     # discount
        self.U  = U     # value function

    def lookahead(self, s, a):
        '''
        computes value at state s taking action a
        '''
        n = np.sum(self.N[s,a,:])
        if (n == 0):
            return 0.0

        r = self.p[s,a]/n

        sum = 0
        for sp in self.S:
            Tsp = self.N[s,a,sp] / n
            sum += Tsp*self.U[sp]

        return r + self.y * sum

    def backup(self, s):
        U_max = -inf
        for a in self.A:
            U_a = self.lookahead(s,a)
            if U_max < U_a:
                U_max = U_a
        return U_max

    def update(self, s, a, r, sp):
        self.N[s,a,sp] += 1
        self.p[s,a] += r

    def MDP(self):
        T = np.zeros(np.shape(self.N))
        R = np.zeros(np.shape(self.p))
        for s in self.S:
            for a in self.A:
                n = np.sum(self.N[s,a,:])
                if n != 0:
                    T[s,a,:] = self.N[s,a,:] / n
                    R[s,a] = self.p[s,a] / n
        return T, R, self.y


    




