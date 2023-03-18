import pandas as pd
import wordle
import wordle
import utils as u
import numpy as np
import MonteCarlo as mc
from numpy import sqrt
import display as dsp

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
        makes a random first guess from wordle dictionary
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
        for _, word in self.wordle_dict.iterrows():
            test = wordle.Wordle(word = self._to_string(word), real_words = True)
            test_results = test.send_guess(self.guess) 
            if results == test_results:
                word_list = word_list.append(word)
        self.wordle_dict = word_list

    def TR(self, s, a, target):
        game = wordle.Wordle(word = target, real_words = True)
        results_prev = game.send_guess(s)
        results = game.send_guess(a)
        count_prev = 0
        count = 0
        for _, word in self.wordle_dict.iterrows():
            test = wordle.Wordle(word = self._to_string(word), real_words = True)

            if s != '-----':
                test_results_prev = test.send_guess(s) 
                if results_prev == test_results_prev:
                    count_prev += 1
            else:
                count_prev = len(self.wordle_dict)

            test_results = test.send_guess(a)
            if results == test_results:
                count += 1
        r = count_prev - count
        s_prime = a
        return s_prime, r

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
        s = ('-----')
        for i in range(len(self.wordle_dict)):
            word = self._to_string(self.wordle_dict.iloc[i])
            S.append(word)
            A.append(word)
            U[word] = 0
        S.append('-----')
        U['-----'] = 0
        
        self.b = list(np.ones(len(S))/len(S))
        self.h = ()
        self.MDP = mc.MDP(
            S, 
            A, 
            [], 
            [],
            y = 0.7, # discount factor
            U = U, 
            TR = self.TR)
        self.MC = mc.MonteCarloTreeSearch(
            N = {}, 
            Q = {}, 
            d = 6, # depth
            m = 2000, # number of simulations
            c = 5, # exploration constant
            U = self.MDP.U,
            P = self.MDP
            )
        self.guess = self.MC.monte_carlo(s)

    def make_guess(self, results, s):
        '''
        makes guess based on results and belief updates
        returns guess as str()
        '''
        # update belief using particle filter
        # determine next action based on Monti Carlo Tree search
                # make optimal first guess
        # TODO: data analysis + learning to determine optimal first guess
        self.wordicle_filter(results)
        S = []
        A = []
        U = {}
        for i in range(len(self.wordle_dict)):
            word = self._to_string(self.wordle_dict.iloc[i])
            S.append(word)
            A.append(word)
            U[word] = 0
        self.MDP = mc.MDP(
            S, 
            A, 
            [], 
            [],
            y = 0.7, # discount factor
            U = U, 
            TR = self.TR)
        S.append(s)
        U[s] = 0
        self.MC = mc.MonteCarloTreeSearch(
            N = {}, 
            Q = {}, 
            d = 6, 
            m = len(A)*len(S), 
            c = 5, 
            U = self.MDP.U,
            P = self.MDP
            )
        self.MC.d -= 1
        self.guess = self.MC.monte_carlo(s)

if __name__ == "__main__":
    disp = dsp.Display()
    runs = 1000 # number of games played
    if True:
        if False:
            this = WordlePro("_small")
            # game = wordle.Wordle(word = 'hello', real_words = True)
            # small.csv guess = 'sells'
            # game = wordle.Wordle(word = 'early', real_words = True)
            this.make_first_guess()
            first_guess = this.guess
        else:
            first_guess = 'ropes' #small
            # first_guess = 'boers' #xsmall

        count_list = []
        for i in range(runs):
            disp.reset_count()
            this = WordlePro("_small")
            game = wordle.Wordle(word = this.get_random_word(), real_words = True)
            this.guess = first_guess
            results = game.send_guess(this.guess)
            disp.increment_count()
            # results = game.send_guess(this.make_first_guess())
            for _ in range(6):
                if results[1] == True:
                    break
                this.make_guess(results, this.guess)
                results = game.send_guess(this.guess)
                disp.increment_count()

            print(f'guess is {this.guess}')

        counts_pro = u.frequency_array(disp.count_list)
        
    if True:
        count_list = []
        for i in range(runs):
            count = 0
            this = WordleBrick("_small")
            game = wordle.Wordle(word = this.get_random_word(), real_words = True)
            # game = wordle.Wordle(word = 'hello', real_words = True)
            # game = wordle.Wordle(word = 'metro', real_words = True)
            # results = game.send_guess(this.make_first_guess('recto'))
            results = game.send_guess(this.make_first_guess())
            count += 1
            for guess in range(6):
                if results[1] == True:
                    break
                results = game.send_guess(this.make_guess(results))
                count += 1
            count_list.append(count)
            print(f'wordle is {this.guess}')

        counts_benchmark = u.frequency_array(count_list)

    
    u.plot_guess_count(counts_benchmark, counts_pro)