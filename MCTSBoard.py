import sys
import random
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

    # Prints the current state's board
    def printBoard(self):
        for i in range(9):
            if self.board[i] == 0:
                print("?", end="")
            elif self.board[i] == 1:
                print("X", end="")
            elif self.board[i] == -1:
                print("O", end="")

            if i == 2 or i == 5 or i == 8:
                print("")
            else:
                print(" | ", end="")

    # Returns the opponent (player to make next move)
    def getOpponent(self):
        return self.player * -1

    # Returns list of all possible states achievable from this position
    def getAllPossibleStates(self):
        opponent = self.getOpponent()
        states = []
        for i in range(9):
            if self.board[i] == EMPTY:
                new_board = list(self.board)
                new_board[i] = opponent
                #print(f"New board looks like {new_board} with move {i} opponent {opponent}")
                #input()
                states.append(State(new_board, opponent))

        return states

    # Returns a score evaluating the current state
    def evaluatePosition(self):
        for row in range(0, 3):
            row_total = 0
            col_total = 0
            for col in range(0, 3):
                row_total += self.board[row * 3 + col]
                col_total += self.board[col * 3 + row]
            if row_total == PLAYER1_CONNECT or col_total == PLAYER1_CONNECT:
                #print("Player 1 row col win")
                return PLAYER1_WIN
            elif row_total == PLAYER2_CONNECT or col_total == PLAYER2_CONNECT:
                #print("Player 2 row col win")
                return PLAYER2_WIN
            
            diag1 = self.board[0] + self.board[4] + self.board[8]
            diag2 = self.board[2] + self.board[4] + self.board[6]

            if diag1 == PLAYER1_CONNECT or diag2 == PLAYER1_CONNECT:
                #print("Player 1 diag win")
                return PLAYER1_WIN
            elif diag1 == PLAYER2_CONNECT or diag2 == PLAYER2_CONNECT:
                #print("Player 2 diag win")
                return PLAYER2_WIN
        #print("Draw")
        return DRAW

    # Returns True/False if this is a terminal state
    def isTerminal(self):
        if self.evaluatePosition() != DRAW:
            #print("Terminal")
            return True
        
        for square in self.board:
            if square == 0:
                #print("Not terminal")
                return False
        
        return True
    
    # Makes a random legal move and toggles the player. Used for simulations
    def makeRandomMove(self):
        self.player = -self.player
        legal_moves = [square for (square, status) in enumerate(self.board) if status == EMPTY]
        self.board[random.choice(legal_moves)] = self.player
    