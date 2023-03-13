import pandas as pd
import wordle
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

    def _to_row(self, guess):
        this_row = pd.DataFrame(columns=self.wordle_dict.columns)

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

if __name__ == "__main__":
    this = WordleBrick()
    status = False

    while status == False:
        game = wordle.Wordle(random_daily=True, real_words = True)
        # game = wordle.Wordle(word = 'hello', real_words = True)
        # game = wordle.Wordle(word = 'metro', real_words = True)
        # results = game.send_guess(this.make_first_guess('recto'))
        results = game.send_guess(this.make_first_guess())

        for guess in range(6):
            if results[1] == True:
                status = True
                break
            results = game.send_guess(this.make_guess(results))
            
    print(f'Wordle is {this.guess}')