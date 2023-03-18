import numpy as np

class Display():
    def __init__(self):
        self.count = 0
        self.count_list = []

    def status_hub(self,i,m,s,Q_max):
        progress = np.round(100*i/m)
        print(f'|{progress}%|[{self.count}]\tCurrent Target Word: [{s}]\tCurrent Q_max: [{Q_max}]')

    def reset_count(self, count = 0):
        self.count_list.append(self.count)
        self.count = 0
    
    def increment_count(self):
        self.count += 1

    def get_count_list(self):
        print(self.count_list)