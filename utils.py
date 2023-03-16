import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def make_plot(data, bins):
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=data, bins=bins, color='#0504aa',
                                alpha=0.85, rwidth=0.85)
    plt.grid(axis='y', alpha=1)
    plt.xlabel('Letter')
    plt.ylabel('Frequency')
    plt.title('Letter Frequency')
    #plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()