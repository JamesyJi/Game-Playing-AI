'''Implements minimax during selection/tree traversal phase to determine forced
wins and losses'''

import sys
import math
import random
import copy
import time
from operator import attrgetter
from MCTSMMAB5x5Board import (
    PLAYER1, PLAYER2, DRAW, PLAYER1_WIN, PLAYER2_WIN, START_BOARD, State,
)

#sims = 0

MAX_INT = float('inf')
MIN_INT = float('-inf')
DEPTH = 4
N_VISITS = 2

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
        print(self.parent.visits)
        return (self.value/(self.visits + 1) + 1.41 * math.sqrt(math.log(self.parent.visits)/(self.visits + 1)))

'''Start of our subtree'''
class Tree:
    def __init__(self, node):
        self.root = node

'''Selects the most promising child node until we reach a leaf node'''
def select_best_child(node):
    #lobal sims
    best_child = node
    while best_child.children:
        children = [children.getNodeScore() for children in best_child.children]
        best_child = best_child.children[children.index(max(children))]

        # Perform mini max after a certain number of visits
        if best_child.visits == N_VISITS:
            #sims += 1
            forced_outcome = minimax(best_child.state, DEPTH, MIN_INT, MAX_INT, best_child.state.player)
            if forced_outcome == best_child.state.player:
                best_child.parent.value = MIN_INT
                best_child.value = MAX_INT
            elif forced_outcome == -best_child.state.player:
                best_child.value = MIN_INT

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
loss 1 ply ahead, ensure we never play it.'''
# NOTE: We will perform minimax to check 2 turns ahead for forced wins/losses
def simulate(node):
    simulate_board = copy.copy(node.state.board)
    simulate_state = State(simulate_board, node.state.player, node.state.last_move)    

    # NOTE: If all child are forced losses, then this node is a forced win.

    # Simulate as normal
    while not simulate_state.isTerminal():
        rollout_policy(simulate_state)

    evaluation = simulate_state.evaluatePosition()
    del simulate_state
    return evaluation

# Minimax 4 ply to check for forced wins/losses 2 turns ahead
def minimax(state, depth, alpha, beta, player):
    if depth == 0 or state.isTerminal():
        return state.evaluatePosition()
    
    last_move = state.last_move

    if player == PLAYER2:
        max_evaluation = MIN_INT
        for move in state.getAllPossibleMoves():
            state.makeMove(move)
            evaluation = minimax(state, depth - 1, alpha, beta, 1)
            state.undoMove(move, last_move)
            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_evaluation
    else:
        min_evaluation = MAX_INT
        for move in state.getAllPossibleMoves():
            state.makeMove(move)
            evaluation = minimax(state, depth - 1, alpha, beta, -1)
            state.undoMove(move, last_move)
            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_evaluation


'''Rollout policy'''
# Try to simulate best move via minimax
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
    t_end = time.time() + time_limit
    #global sims
    # sims = 0
    i = 0
    while time.time() < t_end:
        i += 1
        #print(sims)
        '''SELECTION'''
        # PERFORMS MINIMAX ON STATES AFTER N_VISITS.
        promising_node = select_best_child(root_node)

        '''EXPANSION'''
        #print("Expansion")
        if not promising_node.state.isTerminal():
            expand_node(promising_node)
        
        '''SIMULATION'''
        # Try to run simulation on child. If no child exists, it means we are
        # at a terminal node. Run simulation on the terminal node.
        # print("Simulation")
        if promising_node.children:
            explore_node = promising_node.getRandomChild()
        else:
            explore_node = promising_node

        evaluation = simulate(explore_node)

        '''BACK PROPAGATION'''
        #print("Back propagation")
        back_propagate(explore_node, evaluation)
    '''
    for children in root_node.children:
        children.state.printBoard()
        print(f"had {children.value} wins out of {children.visits} attempts")
    '''
    # Return the best child
    print(f"{i} simulations")
    best_node = root_node.getMostVisitedChild()
    # print(f"Best node selected had {best_node.visits} visits")
    #print(f"NUMBER OF MIN MAXES = {sims}")
    return best_node

'''Player enters a move from the current node'''
def player_move(root_node, player):
    # Selects child of root_node with the move if it exists. If no children,
    # we create a new node and return it as the new root.

    print("Your turn. Enter a number from 1-25")

    legal_moves = root_node.state.getAllPossibleMoves()
    #print(legal_moves)
    while True:
        move = int(input()) - 1
        if move not in legal_moves:
            print("That is an illegal move, try again!")
        else:
            break

    move_node = None
    if root_node.children:
        for child in root_node.children:
            if child.state.board[move] == player:
                move_node = child
                move_node.parent = None
    else:
        board = copy.copy(root_node.state.board)
        board[move] = player
        state = State(board, player, move)
        move_node = Node(state)

    return move_node


if __name__ == "__main__":
    results = []
    # for games in range(1):
        
    print("Press 1 to go first, 2 to go second")
    player = int(input()) 
    if player == 2:
        player = -1
    
    print("How many seconds would you like to give the computer to think?")
    time_limit = int(input())

    # Initialise a new tree
    start_state = State(START_BOARD, PLAYER2)
    root_node = Node(start_state)
    root_node.state.printBoard()
    print("========================================================")
    print("Starting a new game of tic tac toe. Player 1 moves first")
    print("========================================================")

    while not root_node.state.isTerminal():
        if root_node.state.player == player:
            print("Computer Deciding Move==================================================")
            root_node = decide_move(root_node, time_limit)
            #print(f"Parent root node had {root_node.parent.value} wins out of {root_node.parent.visits}")
            #root_node.parent.state.printBoard()
            root_node.parent = None
            #print(f"Selected best root node which had {root_node.value} wins out of {root_node.visits} attempts")
            #root_node.state.printBoard()
            #input()
        else:
            root_node = player_move(root_node, player)
        
        root_node.state.printBoard()

        #results.append(root_node.state.evaluatePosition())
        #del root_node

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
    
    #print(f"Results were player1: {player1_win} draws: {draw} player2: {player2_win}")