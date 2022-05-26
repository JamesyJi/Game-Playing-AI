UPDATE: This was a fun project I worked on in my spare time. I'm currently researching it under Professor Michael Thielscher at UNSW. Here is the new repository with much faster C++ implementation https://github.com/JamesyJi/Thesis-MCTS-GGP

# Game-Playing AI
In this repository, I have combined Monte Carlos Tree Search + Minimax Alpha Beta pruning to play different board games. Currently there exists 3x3 TicTacToe and 5x5 (4-in-a-row) games, however, the algorithms can be applied to any perfect information 2 player games (and really, anything which requires state evaluations).

Currently, the c implementation is out of order as I am implementing a memory freeing algorithm in anticipation of further scaling up the games.

The python versions work (some of them run simulations between 2 AI players, some of them let you play against the AI, run them yourself with python3.

## A Quick Rundown of MCTS ##
The Monte Carlos Tree Search makes state evaluations via randomly simulating moves until an end state is reached (whether this be a predetermined number of moves ahead or until the game ends, etc). It will evaluate that state and then backpropagate the reward. The algorithm balances reward and exploration to ensure that it explores the best moves whilst not neglecting any other moves. After a time limit or a predetermined number of explorations, the algorithm will make its move by picking the state with the highest reward. The process is then repeated.

The intuition behind this is that MCTS converges to a minimax as the number of simulations nears infinity due to the law of large numbers. For example, imagine you are playing a game of chess. You have multiple possible moves but which one do you choose? MCTS performs random simulations on all of those moves. Let's say that in 80% of the simulations where you move your knight, you win. Even though the simulations may be random, this suggests that there is something about moving your knight that leads to an advantageous situation. 

However, there are some pitfalls to this strategy. What if in a particular position, 9/10 moves loses you the game but the one move will lead you to a winning position? This is actually a good position because you have control over your move and you can choose to make that winning move. However, via random simulation, you will find that this position has a 90% losing chance and thus, the algorithm will never see this state as good. In order to deal with things like this, we will implement a minimax lookahead.

## A Quick Rundown on Minimax Alpha Beta pruning ##
Minimax is basically a brute force search method where each player aims to make the best possible move for them. Essentially, it does a brute search with optimal play and can essentially determine, with perfect knowledge, all game states and their possible outcomes. However, it is exponentially expensive which is why we will only use it to augment our MCTS rather than as the main driving algorithm.

Furthermore, we will implement alpha beta pruning to improve efficiency. Again, there are much better explanations online but the gist of alpha beta pruning is that you save a lot of time by ignoring nodes which you have already determined to be worse off than your current best option.

## Combining both algorithms ##
A minimax lookahead can help us determine forced wins/losses in the MCTS search. For example, the previous problematic scenario we described will no longer occur since minimax will help detect that 1/10 forced winning move and thus, let us know that this is a completely won position.

Furthermore, minimax can drastically improve MCTS efficiency by letting it know of forced losses which will tell the algorithm to not bother wasting time exploring nodes which lead to a definite loss.

The issue remaining is with which stage of MCTS to implement the minimax and what depth should we allow it to look ahead? From rough theory and play tests, it seems that minimax is best applied in the selection/tree traversal phase. I will explore this more in the future but currently, applying it in the exploration phase seems to result in very poor performance due to too much computational power required to minimax at every move. Instead, applying it during selection allows the algorithm to be "smart" about which nodes it chooses to explore (i.e. if a node is a forced loss, don't explore it).

## Future improvements ##
Some possible improvements include exploiting the symmetrical nature of the game, tabular reinforcement learning, etc. However the biggest improvement of all seems to be a **neural network**.

Currently, we can only evaluate how good a state is by simulating until the end (i.e. until an end result is achieved). Imagine a game like chess where games often last 40+ moves. Simulating that far into the future is very costly. However, a neural network could allow us to simulate to a much shallower depth and then simply "evaluate" the position via the network, then backpropagate that evaluation back up. If I have time in the future, this will definitely be on my priority list.
