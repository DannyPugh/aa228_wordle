import struct
import numpy as np
import pandas as pd
import wordle

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

class WordleBrick(WordleDict):

    def make_first_guess(self):
        '''
        makes a randoem first guess from wordle dictionary
        '''
        self.guess = self.get_random_word()
        self.green = [' ',' ',' ',' ',' ']
        self.yellow = [' ',' ',' ',' ',' ']
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
        df = pd.DataFrame()
        for i, o in enumerate(results):
            if o == 1:
                self.grey.append(o)
            elif 0 == 2:
                self.yellow[i] = o
            else:
                self.green[i] = o

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
for i in this.wordle_dict.columns:
    print(i)
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

