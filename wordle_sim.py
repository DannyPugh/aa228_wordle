import pandas as pd
import wordle
import wordle
import utils as u
import numpy as np
import MonteCarlo as mc
from numpy import sqrt

class WordleDict:
    '''
    Class with wordle dictionary and some functionality around it
    '''
    def __init__(self, dict = ''):
        '''
        class for holding information about wordle dictionary
        '''
        self.wordle_dict = pd.read_csv(f'wordle_df{dict}.csv', index_col = 0)

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

    def _to_row(self, guess):
        this_row = pd.DataFrame(columns=self.wordle_dict.columns)

    def process_results(self, results):
        r = 0
        o = ''
        results = results[0].split('   ')[0:5]
        for i, letter in enumerate(results):
            if len(letter) == 3:
                r += 10000
                o += 'G'
            else:
                if letter[0].isupper():
                    r += 10
                    o += 'Y'
                else:
                    r += 1
                    o += 'g'
        return o, r

class WordleBrick(WordleDict):

    def make_first_guess(self, guess = ''):
        '''
        makes a randoem first guess from wordle dictionary
        '''
        if guess == '':
            self.guess = self.get_random_word()
        else:
            self.guess = guess
        return self.guess

    def wordicle_filter(self, results):
        word_list = pd.DataFrame(columns=self.wordle_dict.columns)
        for _, word in self.wordle_dict.iterrows():
            test = wordle.Wordle(word = self._to_string(word), real_words = True)
            test_results = test.send_guess(self.guess) 
            if results == test_results:
                word_list = word_list.append(word)
        self.wordle_dict = word_list

    def make_guess(self, results):
        '''
        updates guess based on results
        '''
        self.wordicle_filter(results)
        self.guess = self.get_random_word()
        return self.guess

class WordlePro(WordleDict):
    '''
    plays wordle using optimized methods
    '''

    def wordicle_filter(self, results):
        word_list = pd.DataFrame(columns=self.wordle_dict.columns)
        belief_index = []
        for _, word in self.wordle_dict.iterrows():
            test = wordle.Wordle(word = self._to_string(word), real_words = True)
            test_results = test.send_guess(self.guess) 
            if results == test_results:
                word_list = word_list.append(word)
                belief_index.append(self.POMDP.S.index(self._to_string(word)))
        self.b = list(np.zeros(len(self.POMDP.S)))
        for i in belief_index:
            self.b[i] = 1/len(belief_index)
        self.wordle_dict = word_list

    def TRO(self, s, a):
        game = wordle.Wordle(word = s, real_words = True)
        results = game.send_guess(a)
        o, r = self.process_results(results)
        s_prime = s
        return s_prime, r, o

    def make_first_guess(self):
        '''
        setup MDP and Monte Carlo
        make optimal first guess using Monte Carlo simulation
        '''
        # make optimal first guess
        # TODO: data analysis + learning to determine optimal first guess
        S = []
        A = []
        U = {}
        for i in range(len(self.wordle_dict)):
            word = self._to_string(self.wordle_dict.iloc[i])
            S.append(word)
            A.append(word)
            U[word] = 0
        self.b = list(np.ones(len(S))/len(S))
        self.h = ()
        self.POMDP = mc.POMDP(
            S, 
            A, 
            [], 
            [],
            1, 
            U = U, 
            TRO = self.TRO)
        self.MC = mc.MonteCarloTreeSearch(
            N = {}, 
            Q = {}, 
            d = 6, 
            m = 2000, 
            c = 5, 
            U = self.POMDP.U,
            P = self.POMDP
            )
        self.guess = self.MC.monte_carlo(self.b, self.h)[1]
        return self.guess

    def make_guess(self, results):
        '''
        makes guess based on results and belief updates
        returns guess as str()
        '''
        # update belief using particle filter
        # determine next action based on Monti Carlo Tree search
        self.wordicle_filter(results)
        self.MC.d -= 1
        self.h = (self.guess, self.process_results(results)[0])
        self.guess = self.MC.monte_carlo(self.b, self.h)[1]
        return self.guess




if __name__ == "__main__":

    if True:
        this = WordlePro("_small")
        # game = wordle.Wordle(word = this.get_random_word(), real_words = True)
        # game = wordle.Wordle(word = 'hello', real_words = True)
        game = wordle.Wordle(word = 'early', real_words = True)
        guess = this.make_first_guess()
        results = game.send_guess(guess)
        # results = game.send_guess(this.make_first_guess())
        for guess in range(6):
            if results[1] == True:
                break
            guess = this.make_guess(results)
            results = game.send_guess(guess)
            print(f'guess is {guess}')

    if False:
        count_list = []
        for i in range(100):
            count = 0
            this = WordleBrick("")
            # game = wordle.Wordle(word = this.get_random_word(), real_words = True)
            # game = wordle.Wordle(word = 'hello', real_words = True)
            game = wordle.Wordle(word = 'metro', real_words = True)
            results = game.send_guess(this.make_first_guess('recto'))
            # results = game.send_guess(this.make_first_guess())
            for guess in range(6):
                if results[1] == True:
                    break
                results = game.send_guess(this.make_guess(results))
                count += 1
            count_list.append(count)
            print(f'wordle is {this.guess}')

        u.make_plot(count_list, 5)