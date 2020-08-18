import sys
import math
import random
import copy
import time
import timeit
from operator import attrgetter
from Board1 import (
    PLAYER1, PLAYER2, DRAW, PLAYER1_WIN, PLAYER2_WIN, EMPTY, State,
    getAllPossibleStates, evaluatePosition, isTerminal, makeRandomMove, printBoard, getOpponent

)

global tracknode
import_module = "import copy"
testcode = '''
def test():
    temp_node = copy.deepcopy(tracknode)
'''

MAX_INT = float('inf')
MIN_INT = float('-inf')

'''Contains our node details which holds state which holds boards and game info'''
# State contains information on the board and the player who moved into this turn
class Node:
    def __init__(self, state, parent = None):
        self.state = state # State object
        self.parent = parent
        self.children = []
        self.v = 0
        self.n = 0


def getRandomChild(node):
    return random.choice(node.children)

# Returns the most visited child
def getMostVisitedChild(node):
    return node.children[node.children.index(max(node.children, key=attrgetter('n')))]

# Returns the score of this node
def getNodeScore(node):
    if node.n == 0:
        return MAX_INT
    else:
        return (node.v/node.n + 1.41 * math.sqrt(math.log(node.parent.n)/node.n))


'''Selects the most promising child node until we reach a leaf node'''
def select_best_child(node):
    best_child = node
    while best_child.children:
        children = [getNodeScore(children) for children in best_child.children]
        # print(children)
        best_child = best_child.children[children.index(max(children))]
    return best_child

'''Expands the node, adding children'''
def expand_node(node):
    #start_time = time.time()
    possible_states = getAllPossibleStates(node.state)
    opponent = getOpponent(node.state)
    # print(f"Found {len(possible_states)} states")
    for state in possible_states:
        new_child = Node(state, node)
        new_child.state.player = opponent
        node.children.append(new_child)
    #end_time = time.time()
    #print(f"Expansion took {end_time - start_time}")

'''Runs a simulation based on our rollout policy. If making a move leads to a
loss 1 ply ahead, ensure we never play  it.'''
# No need to simulate at terminal node
#evaluation = evaluatePosition(node.state)
#if isTerminal(node.state) and evaluation == node.state.player:
    # node.state.printBoard()
#    node.parent.v = MIN_INT
#    return evaluation
def simulate(node):
    #tracknode = node
    #print(timeit.timeit(stmt=testcode, setup=import_module, number=1000000))
    #input()
    #printBoard(node.state)
    #print(sys.getsizeof(node))
    start_time = time.time()
    parent = node.parent
    node.parent = None
    node_temp = copy.deepcopy(node)
    node.parent = parent
    #node_temp = node
    end3_time = time.time()

    print(f"Copying took {end3_time - start_time}")

    while not isTerminal(node_temp.state):
        node_temp = rollout_policy(node_temp)
    #end_time = time.time()
    #print(f"Simulation took {end_time - end3_time}")
    evaluation = evaluatePosition(node_temp.state)
    #end_time2 = time.time()
    #print(f"Took {end_time2 - end_time} to evaluate the move")
    del node_temp

    print("Finished simulation")
    printBoard(node.state)
    # input()
    return evaluation

def legal_moves(node):
    moves = []
    for i in range(9):
        if node.state.board[i] == 0:
            moves.append(i)
    return moves

# Our rollout policy CURRENTLY ON RANDOM PLAYOUT
# NOTE: In future, we can make an evaluation of 1 ply with getAllPossibleStates
def rollout_policy(node):
    moves = legal_moves(node)
    move = random.choice(moves)
    node.state.board[move] = -node.state.player
    node.state.player *= -1
   # start_time = time.time()
   # makeRandomMove(node.state)
   # end_time = time.time()
   # print(f"Rollout took {end_time - start_time}")
   # node.state.printBoard()
   # input()
    return node



'''Back propagates, updating scores until root'''
def back_propagate(node, evaluation):
    current_node = node
    while current_node != None:
        if current_node.state.player == evaluation:
            current_node.v += 1 # This player won
        elif current_node.state.player == -evaluation:
            current_node.v -= 1 # This player lost

        # TODO: Contidion to also update draw scores?
        current_node.n += 1
        current_node = current_node.parent

test_state = State([1, 0, 0, 0, 0, 0, 0, 0, 0], -1)
test_node = Node(test_state)
def f1():
    temp_node = copy.deepcopy(test_node)
    del temp_node

'''Applies MCTS to determine the best node to move into'''
def decide_move(root_node, time_limit):
    # Go through the four phases of MCTS within our time condition
    t_end = time.time() + time_limit
    while time.time() < t_end:
        '''SELECTION'''
        #print("Selection")
        promising_node = select_best_child(root_node)

        '''EXPANSION'''
        #print("Expansion")
        if not isTerminal(promising_node.state):
            # print("EXPANDING")
            expand_node(promising_node)

        '''SIMULATION'''
        # Try to run simulation on child. If no child exists, it means we are
        # at a terminal node. Run simulation on the terminal node.
        #print("Simulation")
        if promising_node.children:
            explore_node = getRandomChild(promising_node)
        else:
            explore_node = promising_node
        #printBoard(explore_node.state)
    
        evaluation = simulate(explore_node)
        #print(timeit.timeit(f1, number = 1))
        #input()

        '''BACK PROPAGATION'''
        #print("Back propagation")
        back_propagate(explore_node, evaluation)
        
    for children in root_node.children:
        printBoard(children.state)
        print(f"had {children.v} wins out of {children.n} attempts")
    # Return the best child
    best_node = getMostVisitedChild(root_node)
    # print(f"Best node selected had {best_node.n} n")
    return best_node


if __name__ == "__main__":
    results = []
    for games in range(20): 
        # Initialise a new tree
        start_state = State([0, 0, 0, 0, 0, 0, 0, 0, 0], -1)
        root_node = Node(start_state)
        #root_node.state.printBoard()

        print("========================================================")
        print("Starting a new game of tic tac toe. Player 1 moves first")
        print("========================================================")

        while not isTerminal(root_node.state):
            print("Deciding move==================================================")
            root_node = decide_move(root_node, 5)
            root_node.parent = None
            print("Selected best root node which was")
            printBoard(root_node.state)
            input()
        results.append(evaluatePosition(root_node.state))
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