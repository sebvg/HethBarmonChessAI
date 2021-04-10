A simple chess engine written using python and the python chess library.
"chessAI2.py" is the working version which using a parametric evaluation function, and
a minimax with alpha beta pruning search algorithm, as well as an opening database.
The depth is set to 4 currently - anything higher runs slowly on my machine.
The AI isn't terrible, but should lose to most human players.

"chessAI2.py" is an attempt at the same search algorithm using a convolutional
neural network to evaluate positions. The network was trained on chess positions from
engine games to predict the outcome of the games from a random position after move 5.
While the neural net has an out-of-sample accuracy of around 65%, this simply isn't
good enough to make the engine work, and the engine plays terribly.