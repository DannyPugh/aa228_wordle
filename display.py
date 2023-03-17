import numpy as np

def status_hub(i,m,s,Q_max):
    progress = np.round(100*i/m)
    print(f'|{progress}%|\tCurrent Target Word: [{s}]\tCurrent Q_max: [{Q_max}]')