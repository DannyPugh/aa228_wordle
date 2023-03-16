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

def visualize_map(data, rotate = False):
    fig, ax = plt.subplots()
    if rotate == False:
        ax.imshow(data)
    else:
        ax.imshow(data)

def get_state_space(n): # where n is the number of letters in our alphabet
    return (1+2+3+4+5+6)*((3*n)**5)

def make_wordle_csv():
    df = open('wordle_dict.csv')
    df = df.read()
    df = df.lower()
    df = df.replace(',','')
    df = df.replace('\'','')
    tmp = np.array(list(df))
    df = np.reshape(tmp, [int(len(tmp)/5),5])
    df = pd.DataFrame(df)

    df.to_csv('wordle_df.csv')

def rows_contain(letter, df):
    frame = []
    for col in df.columns:
        tmp_df = df[df[col] == letter]
        frame.append(tmp_df)
    new_df = pd.concat(frame)
    return new_df

def rows_contain_multi(letters, df):
    vowels = ['a','e','i','o','u','y']
    letters = letters + vowels
    frame = []
    for col in df.columns:
        letter_frame = []
        for letter in letters:
            tmp_df = df[df[col] == letter]
            letter_frame.append(tmp_df)
        frame.append(pd.concat(letter_frame))
        df = pd.concat(letter_frame)
    return df

def get_stats(df):
    stats = pd.DataFrame(columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
       'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
       'z'])
    for i in df.columns:
        letter_count = np.zeros(26)
        for index, letter in enumerate(stats.columns):
            size = df[df[i]==letter][i].size
            letter_count[index] = size
        stats.loc[len(stats)] = list(letter_count)
    return stats

def find_argmax(df, exclude = []):
    stats = get_stats(df)
    # convert to array
    arr = np.asarray(stats)
    letter_sum  = arr.sum(0)
    letter_sum[ord('a')-ord('a')]=0
    letter_sum[ord('e')-ord('a')]=0
    letter_sum[ord('i')-ord('a')]=0
    letter_sum[ord('o')-ord('a')]=0
    letter_sum[ord('u')-ord('a')]=0
    #remove exclude letters
    if exclude != []:
        for i in exclude:
            letter_sum[ord(i)-ord('a')]=0
    return chr(letter_sum.argmax()+ord('a'))


df = pd.read_csv('wordle_df.csv', index_col = 0)

max_list = []
for i in range(3):
    max_list.append(find_argmax(df, max_list))
print(max_list)

df = rows_contain_multi(max_list,df)

df = df.sort_index()
df.to_csv('wordle_df_small.csv')

stats = get_stats(df)
visualize_map(stats)
plt.show()



# df = rows_contain('s',df)

# data = df['0']
# make_plot(data)
# plt.show()

print('done')
