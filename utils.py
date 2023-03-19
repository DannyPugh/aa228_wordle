import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from itertools import product
# from sklearn import preprocessing

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


def get_product(list_1, depth):
    '''
    returns list of all combinations of list items to specified depth
    '''
    prods = product(list_1, repeat = depth)
    return list(prods)

def get_comb_list(list_1, list_2):
    '''
    returns combinations list
    '''
    unique_combinations = []
    for item_1 in list_1:
        for item_2 in list_2:
            unique_combinations.append((item_1,item_2))
    return unique_combinations

def plot_guess_count(benchmark_counts, mc_counts):
    
    barWidth = 0.35 # set width of bar
    x = range(1,7)

    df = pd.DataFrame({'benchmark': benchmark_counts[:,0], 'monte carlo': mc_counts[:,0]})
    df.to_csv('1000Runs_RandWord_C2.csv')
    
    
    # Set position of bar on X axis
    br1 = np.arange(len(benchmark_counts[:,0]))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    plt.bar(br1, benchmark_counts[:,0], color ='b', width = barWidth,
            edgecolor ='grey', label ='Benchmark Counts')
    plt.bar(br2, mc_counts[:,0], color ='g', width = barWidth,
            edgecolor ='grey', label ='Monte Carlo Counts')


    # Adding Xticks
    plt.xlabel('Guess Distribution', fontweight ='bold', fontsize = 15)
    plt.ylabel('Frequency', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth/2 for r in range(len(benchmark_counts[:,0]))],
            ['1', '2', '3', '4', '5', '6'])
    
    plt.legend()
    plt.show()

def frequency_array(arr):
    freq_arr = np.zeros((6, 1), dtype=int) # Initialize an array of zeros with size 5x1

    for num in arr:
        if num == 1:
            freq_arr[0] += 1
        elif num == 2:
            freq_arr[1] += 1
        elif num == 3:
            freq_arr[2] += 1
        elif num == 4:
            freq_arr[3] += 1
        elif num == 5:
            freq_arr[4] += 1
        elif num == 6:
            freq_arr[5] += 1
    
    return freq_arr