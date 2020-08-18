import sys
import random
from colorama import Fore, Style

EMPTY = 0
PLAYER1 = 1
PLAYER2 = -1
PLAYER1_WIN = 1
PLAYER2_WIN = -1
PLAYER1_CONNECT = 4
PLAYER2_CONNECT = -4
DRAW = 0
START_BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
'''Contains data regarding state of this game position. Holds information about Board'''
# Player refers to player who made the move to get into this state
class State:
    def __init__(self, board, player, last_move = None):
        self.player = player
        self.board = board
        self.last_move = last_move # Helps us evaluate the position easier

    # Prints the current state's board
    def printBoard(self):
        for i in range(25):
            if self.board[i] == 0:
                print(f"?", end="")
            elif self.board[i] == 1:
                print(f"{Fore.BLUE}X{Style.RESET_ALL}", end="")
            elif self.board[i] == -1:
                print(f"{Fore.RED}O{Style.RESET_ALL}", end="")

            

            if i in [4, 9, 14, 19, 24]:
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
        for move in range(25):
            if self.board[move] == EMPTY:
                new_board = list(self.board)
                new_board[move] = opponent
                #print(f"New board looks like {new_board} with move {i} opponent {opponent}")
                #input()
                states.append(State(new_board, opponent, move))

        return states

    # Returns a list of possible moves
    def getAllPossibleMoves(self):
        moves = []
        for i in range(25):
            if self.board[i] == EMPTY:
                moves.append(i)
        return moves

    # Makes a move
    def makeMove(self, move):
        self.player = -self.player
        self.board[move] = self.player
        self.last_move = move

    # Undoes a move
    def undoMove(self, move, last_move):
        self.player = -self.player
        self.board[move] = EMPTY
        self.last_move = last_move

    # Returns a score evaluating the current state
    def evaluatePosition(self):
        if self.last_move == None:
            return DRAW
        
        # Get the row (multiple of 5) and column of the last move
        last_col = self.last_move % 5
        last_row = self.last_move - last_col

        # Calculate if the row was won
        row_col_wins = []
        row_col_wins.append(self.board[last_row] + self.board[last_row + 1] + self.board[last_row + 2] + self.board[last_row + 3])
        row_col_wins.append(self.board[last_row + 1] + self.board[last_row + 2] + self.board[last_row + 3] + self.board[last_row + 4])
        row_col_wins.append(self.board[last_col] + self.board[last_col + 5] + self.board[last_col + 10] + self.board[last_col + 15])
        row_col_wins.append(self.board[last_col + 5] + self.board[last_col + 10] + self.board[last_col + 15] + self.board[last_col + 20])

        if max(row_col_wins) == PLAYER1_CONNECT:
            return PLAYER1_WIN
        elif min(row_col_wins) == PLAYER2_CONNECT:
            return PLAYER2_WIN

        diagonals = []
        diagonals.append(self.board[0] + self.board[6] + self.board[12] + self.board[18])
        diagonals.append(self.board[6] + self.board[12] + self.board[18] + self.board[24])
        diagonals.append(self.board[4] + self.board[8] + self.board[12] + self.board[16])
        diagonals.append(self.board[8] + self.board[12] + self.board[16] + self.board[20])
        diagonals.append(self.board[1] + self.board[7] + self.board[13] + self.board[19])
        diagonals.append(self.board[5] + self.board[11] + self.board[17] + self.board[23])
        diagonals.append(self.board[3] + self.board[7] + self.board[11] + self.board[15])
        diagonals.append(self.board[9] + self.board[13] + self.board[17] + self.board[21])
        #print(f"Diagonal scores are {diagonals}")
        if max(diagonals) == PLAYER1_CONNECT:
            return PLAYER1_WIN
        elif min(diagonals) == PLAYER2_CONNECT:
            return PLAYER2_WIN

        #print("Draw")
        return DRAW

    # Returns True/False if this is a terminal state
    def isTerminal(self):
        if self.evaluatePosition() != DRAW:
            #print("Terminal")
            return True
        
        for square in self.board:
            if square == EMPTY:
                #print("Not terminal")
                return False
        
        return True
    
    # Makes a random legal move and toggles the player. Used for simulations
    def makeRandomMove(self):
        self.player = -self.player
        legal_moves = [square for (square, status) in enumerate(self.board) if status == EMPTY]
        move = random.choice(legal_moves)
        self.board[move] = self.player
        self.last_move = move