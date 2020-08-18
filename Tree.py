'''Implementation of tree data structure'''
import sys
import math
import random
import copy
import time
import timeit
from board import (
    BOARD, State, legal_moves, is_terminal, calculate_value, print_board,
)

global tracknode
import_module = "import copy"
testcode = '''
def test():
    temp_node = copy.deepcopy(tracknode)
'''

'''
1. From root, SELECTS child with greatest value until we reach
    a leaf node. (Not fully expanded)
2. EXPAND the leaf node and SIMULATES ONCE for each child.
3. BACK PROPAGATES results of simulation back to root.
4. From root, repeat steps 1-3 until time limit or other end condition.
'''

# Contains details regarding the node
class Node:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.v = 0
        self.n = 0

    # Calculates the score of this node based on a formula
    def score(self):
        return (self.v/self.n + math.sqrt(2)*math.log(self.parent.n)/self.n)

# Select best child until we reach a leaf node.
def select_best_child(node):
    best_child = node
    # print(f"Children of {node.state.board} are:")
    # for child in best_child.children:
        # print(f"{child.state.board}")

    while best_child.children:
        best_child = find_best_child(best_child)

    #print(f"Best child was")
    #print_board(best_child)
    return best_child


# Helper function to find the child with the highest score
def find_best_child(node):
    choices = [children.score() for children in node.children]
    # print(f"Choices are {choices}")
    return node.children[choices.index(max(choices))]

# Expand the leaf node and simulates once for each child.
def expand_node(node):
    #start_time = time.time()
    #print(f"Expanding nodes of")
    #print_board(node)
    # Find a list of all possible moves
    moves = legal_moves(node)
    # print(f"All legal moves are: {moves}")
    # For each move, create a new child node and simulates it once.
    for new_move in moves:
        # Create a child
        # print(f"Creating a child for move {new_move}")
        child = create_child_node(new_move, node)
        node.children.append(child)
        
        # Run simulation for child
        value = simulate(child)
        # print(f"Calculated value {value} for {child.state.board}")
        back_propagate(child, value)
    end_time = time.time()
    #print(f"Expansion took {end_time - start_time}")

# Helper function to create a child node given a move and a parent
def create_child_node(move, parent):
    child_board = list(parent.state.board)
    child_board[move] = parent.state.player
    child_state = State(child_board, parent.state.player * -1)
    child = Node(child_state, parent)
    #print(f"Checking original parent:")
    # print_board(parent)
    #print(f"Finished creating a child with player {child.state.player}")
    # print_board(child)
    return child 


# Rollout policy simulates until decided game state (terminal)
def simulate(node):
    #tracknode = node
    #print(timeit.timeit(stmt=testcode, setup=import_module, number=1000000))
   # input()
    print_board(node)
    #print(sys.getsizeof(node))
    start_time = time.time()
    parent = node.parent
    node.parent = None
    node_temp = copy.deepcopy(node)
    node.parent = parent
    #node_temp = node
    end3_time = time.time()
    print(f"Copying took {end3_time - start_time}")

    #print(f"Running simulation on")
    #print_board(node)
    while not is_terminal(node_temp):
        node_temp = rollout_policy(node_temp)
    end_time = time.time()
    print(f"Simulation took {end_time - end3_time}")
    value = calculate_value(node_temp)
    end_time2 = time.time()
    print(f"Took {end_time2 - end_time} to evaluate the move")
    del node_temp

    # input()
    return value

# Randomly selects a legal move and updates the gamestate
def rollout_policy(node):
    # start_time = time.time()
    moves = legal_moves(node)
    #print(f"Rolling out moves: {moves}")
    move = random.choice(moves)
    #print(f"Selected random move {move}")
    node.state.board[move] = node.state.player
    node.state.player *= -1

    # finish_time = time.time()
    # print(f"Random move took {finish_time - start_time} to make")

    #print(f"Node now looks like {node.state.board}.")
    # end_time = time.time()
    #print(f"Rollout took {end_time - start_time}")
    # print_board(node)
 #   input()

    return node

# Back propagate and updates until root. Only updates for the player who
# won the game.
def back_propagate(node, value):
    current_node = node
    #print(f"Back propagating on node {node.state.board} with player {node.state.player}")
    #print(f"Back propagating next_player {node.state.player} result {value}")
    #print_board(node)
    while current_node != None:
        '''
        If this move is terminal and there is a winner (let's say -1), then
        that means 1 made a move right before this which leads to a loss.
        As a result, we should very heavily weight that move negatively
        to prevent 1 from making that move.
        '''
        if current_node.state.player == -1 * value:
            current_node.v += 1 # This player won
            if is_terminal(current_node):
                #print("Back propagating a terminal")
                # Make the parent weigh very poorly.
                current_node.parent.v -= 100
        elif current_node.state.player == value:
            current_node.v -= 1
        else:
            current_node.v += 0
        current_node.n += 1

        current_node = current_node.parent

# Find the most visited child given a root node
def most_visited_child(root):
    visits = [children.n for children in root.children]
    return root.children[visits.index(max(visits))]

test_state = State([1, 0, 0, 0, 0, 0, 0, 0, 0], -1)
test_node = Node(test_state)
def f1():
    temp_node = copy.deepcopy(test_node)
    del temp_node

if __name__ == "__main__":
    results = []
    for i in range(1):
        print("====================================================")
        print("Starting a new game of tic tac toe. You are player 1")
        print("====================================================")
        #time.sleep(1)
        start_state = State([0, 0, 0, 0, 0, 0, 0, 0, 0], 1)
        root = Node(start_state)

        while True:
            if is_terminal(root):
                print(f"END OF GAME!!!! {root.state.board}")
                results.append(calculate_value(root))
                del root
                del start_state
                break

            # print(f"Deciding move for 10 seconds")
            # input()
            #time.sleep(1)
            t_end = time.time() + 5
            while time.time() < t_end:
                best_leaf = select_best_child(root)
                expand_node(best_leaf)

                #print(timeit.timeit(f1, number = 1))
                #input()
                # print("Finished expanding")
                value = simulate(best_leaf)
                #print(f"Value is {value}")
                back_propagate(best_leaf, value)
                #print(f"Root values are {root.v} {root.n}")
                #print(f"Best leaf selected {best_leaf.v} {best_leaf.n} was: ")
                #print_board(best_leaf)

            # print(f"Root values are {root.v} {root.n}")
            for children in root.children:
                print_board(children)
                print(f"has {children.v} wins out of {children.n} atttempts")
            '''
            print(f"Root values are {root.v} {root.n}")
            for children in best_leaf.children:
                print(f"Children {children.state.board} has {children.v} {children.n}")
            '''
            
            # Find the best child and then perform analysis with it as root
            root = most_visited_child(root)
            root.parent = None
            print(f"Selected most visited child with value {root.v} out of {root.n} vists")
            print_board(root)
            input()
            #input()


    print("RESULTS WERE====================")
    draws = 0
    first = 0
    second = 0
    for i in results:
        if i == 0:
            draws += 1
        elif i == 1:
            first += 1
        else:
            second += -1
    print(f"First: {first} Draw: {draws} Second: {second}")