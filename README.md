# aa228_wordle
## Use this to get started
to form DataFrame of the wordle dictionary use

```python3 data_analysis.py```

## What is this project?

Using Wordle Library for our model, we are looking into Online planning specifically Monte Carlo Tree Search to build an agent that will learn to play wordle.

model: https://pypi.org/project/wordle-python/



## Update 3-10-23:


basically after talking with the CA last week she recommended having some kind of bench mark case so like something that just make random guesses within the rules of the game and then our optimized agent. She said POMDP has been used for wordle in the past.

also I know we keep switching but I think using the full words in the wordle dictionary as the state space size = n, using a move to a new word as actions size = n (particle filter will reduce these after first guess) and using the green yellow red tiles as our observations would be best.

I created a “WordleBrick” class that will just make a random first guess and update with a random new guess that holds Green tiles tries yellow tiles in a new random place and does not retry grey tiles and replaces with a random new letter


I created a “WordlePro” class that will use particle filtering to determine possible states that match the observations (ie green, yellow, grey, tiles) this is basically what the brick does as well and then uses a Monti Carlo tree search to determine a next guess with the most utility (ie best information). The big hitter will be from the first guess which will come from priors based on an offline search, which we could probably develop using value iteration or something (still need work on this).


this is all what it is supposed to do but I haven’t programmed that much.
TLDR:


program WordleBrick to make random first guess and random guesses give information from results of previous guesses


program WordlePro 

guess based on particle filter to update belief and Mani Carlo search for best action
    
first guess based on value iteration of wordle dictionary state space


