import struct
import numpy as np
import pandas as pd
import wordle
import utils as u

class WordleDict:
    '''
    Class with wordle dictionary and some functionality around it
    '''
    def __init__(self):
        self.wordle_dict = pd.read_csv('wordle_df.csv', index_col = 0)

    def get_random_word(self):
        '''
        returns random word from wordle dictionary
        '''
        word = self.wordle_dict.sample(1).iloc[0]
        return self._to_string(word)

    def _to_string(self, guess):
        this_string = ''
        for letter in list(guess):
            this_string += letter
        return this_string

    def generate_prior(self):
        '''
        process for generating prior
        '''
        #TODO: update this

        state = np.zeros([26,5])

        for i in range(5):
            for j in range(26):
                size = self.wordle_dict[self.wordle_dict[chr(i+48)]==chr(j+97)][chr(i+48)].size
                state[j,i] = size
        return state
    
    def process_results(self, results):
        '''
        processes wordle results as mapping
        '''
        state = np.zeros(5)
        results = results[0].split('   ')[0:5]

        for i, letter in enumerate(results):
            if len(letter) == 3:
                # green
                state[i] = 3
            else:
                if letter[0].isupper():
                    # yellow
                    state[i] = 2
                else:
                    # grey
                    state[i] = 1
        return state 

class WordleBrick(WordleDict):

    def make_first_guess(self):
        '''
        makes a randoem first guess from wordle dictionary
        '''
        self.guess = self.get_random_word()
        self.green = []
        self.yellow = []
        self.grey = []
        return self.guess

    def make_guess(self, results):
        '''
        updates guess based on results
        results - list of five elements
        #   code    strategy
        3   Green   stay
        2   Yellow  switch to a random place
        1   Grey    replace a with random letter
        '''
        df = self.wordle_dict
        for i, o in enumerate(results):
            if o == 3:
                self.green.append((self.guess[i],str(i)))
            elif o == 2:
                if len(self.yellow) != 0:
                    for j in self.yellow:
                        if self.guess[i] == j[0]:
                            j[1].remove(str(i))
                            break
                        else:
                            count = ['0','1','2','3','4']
                            count.remove(count[i])
                            self.yellow.append((self.guess[i],count))
                            break
                else:
                    count = ['0','1','2','3','4']
                    count.remove(count[i])
                    self.yellow.append((self.guess[i],count))
            else:
                self.grey.append(self.guess[i])
        
        count = ['0','1','2','3','4']
        # filter based on grey letters
        for col in df.columns:
            for i in self.grey:
                df = df[df[col]!=i]
        # filter based on green letters
        for i in self.green:
            letter = i[0]
            col = i[1]
            df = df[df[col] == letter]
            count.remove(col)
        # filter yellow
        for i in self.yellow:
            letter = i[0]
            cols = i[1]
            for j in range(5):
                picks = []
                for col in cols:
                    if col in count:
                        picks.append(col)
                col = picks[u.rand((0,len(picks)-1))]
                tmp_df = df[df[col] == letter]
                if tmp_df.size != 0:
                    df = tmp_df
                    count.remove(col)
                    break
        self.wordle_dict = df
        guess = this.get_random_word()
        return guess

class WordlePro(WordleDict):
    '''
    plays wordle using optimized methods
    '''

    def make_first_guess(self):
        '''
        make optimal first guess
        returns guess as str()
        '''
        # make optimal first guess
        # TODO: data analysis + learning to determine optimal first guess
        return "words"

    def make_guess(self, results):
        '''
        makes guess based on results and belief updates
        returns guess as str()
        '''
        # update belief using particle filter
        # determine next action based on Monti Carlo Tree search
        return "words"


this = WordleBrick()
this.make_first_guess()
this.guess = 'recto'
# ground truth = 'metro'

try:
    while True:
        game = wordle.Wordle(word = 'metro', real_words = True)
        results = game.send_guess(this.make_first_guess())
        for guess in range(6):
            results = this.process_results(results)
            results = game.send_guess(this.make_guess(results))
finally:
    print(this.guess)


# this.guess = 'hello'
# this.make_guess([1,3,2,2,3])



# this.make_guess([2,3,1,2,3])

# for i in this.wordle_dict.columns:
#     print(i)
# prior = this.generate_prior()
# print(prior)

# fake_results = ('h   *E*   L   L   o   ', False)

# fake_state = process_results(fake_results)

# print(fake_state)

# print(np.argmax(prior + fake_state, 0)) #factor of isWord()


                


    
 



# def process_results(results):
#     state = np.zeros([26,5])
#     results = results[0].split('   ')[0:5]
#     for i, letter in enumerate(results):
#         if len(letter) == 3:
#             j = ord(letter[1])-65
#             state[j,i] += 10000
#         else:
#             if letter[0].isupper():
#                 j = ord(letter[0])-65
#                 state[j,:] += 500
#                 state[j,i] += -10000
#             else:
#                 j = ord(letter[0])-97
#                 state[j,:] += -10000
#     return state




# try:
#     while True
#         game = wordle.Wordle(word = wordle.random_answer(), real_words = True)
#         results = [0,0,0,0,0]
#         for guess in range(6):
#             results = game.send_guess(make_guess(results))

# def process_results(results):
#     '''
#     processes wordle results as mapping
#     '''
#     state = np.zeros([26,5])
#     results = results[0].split('   ')[0:5]

#     for i, letter in enumerate(results):
#         if len(letter) == 3:
#             # green
#             j = ord(letter[1])-65
#             state[j,:] = np.zeros([1,26])
#             state[j,i] = 3
#         else:
#             if letter[0].isupper():
#                 # yellow
#                 j = ord(letter[0])-65
#                 state[j,:] += 500
#                 state[j,i] += -10000
#             else:
#                 # grey
#                 j = ord(letter[0])-97
#                 state[j,:] += -10000
#     return state 

