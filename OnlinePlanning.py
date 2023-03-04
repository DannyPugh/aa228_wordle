from Math import inf

class OnlinePlanning:
    def __init__(self, P, d, U):
        self.P = P # problem model
        self.d = d # depth of search
        self.U = U # value function @ depth d

    def forward_search(self, s):
        '''
        performs forward search from state s
        '''
        if self.d <= 0:
            return u = self.U(s)

        best = (a = float("nan"), u = -inf):
        

