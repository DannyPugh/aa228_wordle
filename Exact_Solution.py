import numpy as np

class MDP:
    def __init__(self, Y, S, A, T, R):
        self.Y = Y # discount factor
        self.S = S # States
        self.A = A # Actions
        self.T = T # Transition Matrix
        self.R = R # Rewards

    def lookahead(self, s, a):
        '''
        policy evaluation @ state s when taking action a
        '''
        sum = 0
        for sp in self.S:
            sum += self.T[sp,s,a]*self.U[sp]
        return self.R[s,a] + self.Y*sum

    def iterative_policy_evaluation(self, Pi, k_max):
        '''
        policy evaluation for policy Pi to depth k_max
        '''
        self.U = np.zeros(len(self.S))
        for k in range(k_max):
            U = 

A_low = np.roll(np.diag(np.ones(6)*0.15),1, axis=0)
A_upp = np.roll(np.diag(np.ones(6)*0.15),-1, axis=0)
A_mid = np.diag(np.ones(6)*0.7)
A_gw = A_low + A_upp + A_mid

R_sa = np.array([-1,-1,-1,0,-1,-1,0,-1,-1,0,-1,-1,10,10,10,10,10,10,0,0,0,0,0,0])
R_sa = np.reshape(R_sa,[4,6]).T


def compute_value(T, R, y):
    '''
    inputs:
    T - tranformation matrix (S x S)
    R - Reward array (S x 1)
    y - discount scalar
    '''
    # extract number of states
    s = np.shape(T)[0]
    I = np.eye(s)
    U = np.matmul(np.linalg.inv(I - y*T),R)
    return U

def T_ijk(df,s_i,s_j,a_k):
    occur = df[(df['s']==s_i) & (df['a']==a_k)].size
    success = df[(df['s']==s_i) & (df['sp']==s_j) & (df['a']==a_k)].size
    if occur != 0:
        return success/occur
    else:
        return 0

def T_ik(df, s, a):
    T = np.zeros([s,s,a])
    for index, x in np.ndenumerate(T):
        T[index] = T_ijk(df,index[0],index[1],index[2])
    return T

def T_(df, s, a):
    T = np.zeros([s,s,a])
    for index, x in np.ndenumerate(T):
        T[index] = T_ijk(df,index[0],index[1],index[2])
    return T

def R_ik(df,s_i,a_k):
    occur = df[(df['s']==s_i) & (df['a']==a_k)].size
    sum_ = df[(df['s']==s_i) & (df['a']==a_k)]['r'].sum()
    if occur != 0:
        return sum_/occur
    else:
        return 0

def R_(df,s,a):
    R = np.zeros([s,a])
    for index, x in np.ndenumerate(R):
        R[index] = R_ik(df,index[0],index[1])
    return R

def U_(s):
    U = np.zeros([s,1])
    return U

def compute_policy(Q, R, U, y, a, s):
    '''
    inputs:
    T - tranformation matrix (S x S)
    R - Reward array (S x 1)
    U - Expected Value (S x S)
    y - discount scalar
    s - range of states
    a - range of actions
    '''
    #return argmax()
    for s_i in s:
            U_[s_i] = np.max((R[a] + y*Q*U),1)
    return U_



if __name__ == '__main__':
    '''
    solve T(s,a) from df save sparse
    solve R(s,a) from df save sparse
    established a policy for 
    init u = 0
    value iteration to find U


    '''


    # R = np.array([-0.3, -0.85, 10, 0])

    # T = np.reshape(
    # np.array([0.3, 0.7, 0, 0, 0, 0.85, 0.15, 0, 0, 0, 0, 1, 0, 0, 0, 1]), 
    # [4, 4])

    # R = np.array([0,1])

    # # T = np.reshape(
    # # np.array([0.2, 0.8, 0.1, 0.9]), 
    # # [2, 2])
    # T = np.reshape(
    # np.array([0.9, 0.1, 0.2, 0.8]), 
    # [2, 2])

    # y = 0.9

    R = np.array([0,0,0,0,0,0,0,0,0,2])

    # T = np.reshape(
    # np.array([0.2, 0.8, 0.1, 0.9]), 
    # [2, 2])
    R = np.diag(np.ones(10))
    R[8,8] = 0.5
    R[8,9] = 0.5

    y = 0.5

    U = compute_value(R,R,y)
    print(U)
    _U = evaluate_policy(R,R,U,y)
    _U
