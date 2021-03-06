'''Uses MCTS to play on a 5x5 board where you have to connect 4 to win'''
import sys
import math
import random
import copy
import time
from operator import attrgetter
from Board5x5 import (
    PLAYER1, PLAYER2, DRAW, PLAYER1_WIN, PLAYER2_WIN, START_BOARD, State,
)

MAX_INT = float('inf')
MIN_INT = float('-inf')

'''Contains our node details which holds state which holds boards and game info'''
# State contains information on the board and the player who moved into this turn
class Node:
    def __init__(self, state, parent = None):
        self.state = state # State object
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0

    # Returns a random child of the node
    def getRandomChild(self):
        return random.choice(self.children)

    # Returns the most visited child
    def getMostVisitedChild(self):
        return self.children[self.children.index(max(self.children, key=attrgetter('visits')))]

    # Returns the score of this node
    def getNodeScore(self):
        if self.visits == 0:
            return MAX_INT
        else:
            return (self.value/self.visits + 1.41 * math.sqrt(math.log(self.parent.visits)/self.visits))

'''Start of our subtree'''
class Tree:
    def __init__(self, node):
        self.root = node


'''Selects the most promising child node until we reach a leaf node'''
def select_best_child(node):
    best_child = node
    while best_child.children:
        children = [children.getNodeScore() for children in best_child.children]
        # print(children)
        best_child = best_child.children[children.index(max(children))]
    return best_child

'''Expands the node, adding children'''
def expand_node(node):
    possible_states = node.state.getAllPossibleStates()
    opponent = node.state.getOpponent()
    # print(f"Found {len(possible_states)} states")
    for state in possible_states:
        new_child = Node(state, node)
        new_child.state.player = opponent
        node.children.append(new_child)
        

'''Runs a simulation based on our rollout policy. If making a move leads to a
loss 1 ply ahead, ensure we never play  it.'''
def simulate(node):
    # No need to simulate at terminal node
    evaluation = node.state.evaluatePosition()
    if node.state.isTerminal() and evaluation == node.state.player:
        node.parent.value = MIN_INT
        return evaluation

    # Simulate as normal
    simulate_board = copy.copy(node.state.board)
    simulate_state = State(simulate_board, node.state.player, node.state.last_move)
    while not simulate_state.isTerminal():
        rollout_policy(simulate_state)

    evaluation = simulate_state.evaluatePosition()
    del simulate_state
    return evaluation
    
# Our rollout policy CURRENTLY ON RANDOM PLAYOUT
# NOTE: In future, we can make an evaluation of 1 ply with getAllPossibleStates
def rollout_policy(state):
    state.makeRandomMove()

'''Back propagates, updating scores until root'''
def back_propagate(node, evaluation):
    current_node = node
    while current_node != None:
        if current_node.state.player == evaluation:
            current_node.value += 1 # This player won
        elif current_node.state.player == -evaluation:
            current_node.value -= 1 # This player lost

        # TODO: Contidion to also update draw scores?
        current_node.visits += 1
        current_node = current_node.parent



'''Applies MCTS to determine the best node to move into'''
def decide_move(root_node, time_limit):
    # Go through the four phases of MCTS within our time condition
    #t_end = time.time() + time_limit
    #for i in range(10000):
    while time.time() < t_end:
        '''SELECTION'''
        #print("Selection")
        promising_node = select_best_child(root_node)

        '''EXPANSION'''
        #print("Expansion")
        if not promising_node.state.isTerminal():
            expand_node(promising_node)
        
        '''SIMULATION'''
        # Try to run simulation on child. If no child exists, it means we are
        # at a terminal node. Run simulation on the terminal node.
        #print("Simulation")
        if promising_node.children:
            explore_node = promising_node.getRandomChild()
        else:
            explore_node = promising_node

        evaluation = simulate(explore_node)

        '''BACK PROPAGATION'''
        #print("Back propagation")
        back_propagate(explore_node, evaluation)

    # for children in root_node.children:
    #     children.state.printBoard()
    #     print(f"had {children.value} wins out of {children.visits} attempts")
    # Return the best child
    best_node = root_node.getMostVisitedChild()
    # print(f"Best node selected had {best_node.visits} visits")
    return best_node


if __name__ == "__main__":
    results = []
    for games in range(1): 
        # Initialise a new tree
        start_state = State(START_BOARD, PLAYER2)
        root_node = Node(start_state)
        #root_node.state.printBoard()
        #print(start_state.evaluatePosition())
        #input()
        print("========================================================")
        print("Starting a new game of tic tac toe. Player 1 moves first")
        print("========================================================")

        while not root_node.state.isTerminal():
            print("Deciding move==================================================")
            root_node = decide_move(root_node, 5)
            root_node.parent = None
            print("Selected best root node which was")
            root_node.state.printBoard()

        results.append(root_node.state.evaluatePosition())
        del root_node

    player1_win = 0
    player2_win = 0
    draw = 0
    for result in results:
        if result == DRAW:
            draw += 1
        elif result == PLAYER1_WIN:
            player1_win += 1
        elif result == PLAYER2_WIN:
            player2_win += 1
    
    print(f"Results were player1: {player1_win} draws: {draw} player2: {player2_win}")