import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def make_plot(data):
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=data, bins=26, color='#0504aa',
                                alpha=0.85, rwidth=0.85)
    plt.grid(axis='y', alpha=1)
    plt.xlabel('Letter')
    plt.ylabel('Frequency')
    plt.title('Letter Frequency')
    #plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)


df = open('wordle_dict.csv')
df = df.read()
df = df.lower()
df = df.replace(',','')
df = df.replace('\'','')
tmp = np.array(list(df))
df = np.reshape(tmp, [int(len(tmp)/5),5])
df = pd.DataFrame(df)

df.to_csv('wordle_df.csv')

stats = pd.DataFrame(columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
       'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
       'z'])

for i in range(5):
    letter_count = np.zeros(26)
    for index, letter in enumerate(stats.columns):
        size = df[df[i]==letter][i].size
        letter_count[index] = size
    stats.loc[len(stats)] = list(letter_count)



data = df[0]
make_plot(data)
plt.show()

print('done')