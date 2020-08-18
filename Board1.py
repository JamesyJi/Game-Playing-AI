import sys
import random
import time
EMPTY = 0
PLAYER1 = 1
PLAYER2 = -1
PLAYER1_WIN = 1
PLAYER2_WIN = -1
PLAYER1_CONNECT = 3
PLAYER2_CONNECT = -3
DRAW = 0

'''Contains data regarding state of this game position. Holds information about Board'''
# Player refers to player who made the move to get into this state
class State:
    def __init__(self, board, player):
        self.player = player
        self.board = board

# Returns the opponent (player to make next move)
def getOpponent(state):
    return state.player * -1
    

def getAllPossibleStates(state):
    opponent = -state.player
    board = state.board
    states = []
    for i in range(9):
        if board[i] == EMPTY:
            new_board = list(board)
            new_board[i] = opponent
            states.append(State(new_board, opponent))
    return states

def evaluatePosition(state):
    board = state.board
    for row in range(0, 3):
        row_total = 0
        col_total = 0
        for col in range(0, 3):
            row_total += board[row * 3 + col]
            col_total += board[col * 3 + row]
        if row_total == PLAYER1_CONNECT or col_total == PLAYER1_CONNECT:
            #print("Player 1 row col win")
            return PLAYER1_WIN
        elif row_total == PLAYER2_CONNECT or col_total == PLAYER2_CONNECT:
            #print("Player 2 row col win")
            return PLAYER2_WIN
        
        diag1 = board[0] + board[4] + board[8]
        diag2 = board[2] + board[4] + board[6]

        if diag1 == PLAYER1_CONNECT or diag2 == PLAYER1_CONNECT:
            #print("Player 1 diag win")
            return PLAYER1_WIN
        elif diag1 == PLAYER2_CONNECT or diag2 == PLAYER2_CONNECT:
            #print("Player 2 diag win")
            return PLAYER2_WIN
    #print("Draw")
    return DRAW

# Returns True/False if this is a terminal state
def isTerminal(state):
    if evaluatePosition(state) != DRAW:
        #print("Terminal")
        return True
    
    for square in state.board:
        if square == 0:
            #print("Not terminal")
            return False
    
    return True

# Makes a random legal move and toggles the player. Used for simulations
def makeRandomMove(state):
    start_time = time.time()
    state.player = -state.player
    legal_moves = [square for (square, status) in enumerate(state.board) if status == EMPTY]
    state.board[random.choice(legal_moves)] = state.player
    end_time = time.time()
    print(f"Random Move took {end_time-start_time} seconds to make")
    #input()

# Prints the current state's board
def printBoard(state):
    board = state.board
    for i in range(9):
        if board[i] == 0:
            print("?", end="")
        elif board[i] == 1:
            print("X", end="")
        elif board[i] == -1:
            print("O", end="")

        if i == 2 or i == 5 or i == 8:
            print("")
        else:
            print(" | ", end="")