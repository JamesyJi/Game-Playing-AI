'''Contains data regarding board state and functions which determine
board state data'''
BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# Contains details regarding the state of the game at that situation
class State:
    def __init__(self, board, player):
        self.board = board # Board data
        self.player = player # Next player to move
    
#def calculate_value(self):
    # determines
#    pass

# Finds all legal moves and returns as list:
def legal_moves(node):
    moves = []
    for i in range(9):
        if node.state.board[i] == 0:
            moves.append(i)
    return moves

# Calculates if the game has ended at this node
def is_terminal(node):
    # Check if someone has won
    if calculate_value(node) != 0:
        # print(f"{node.state.board} is terminal because someone has won")
        return True
    
    # No one has won. Check if there are squares left 
    for square in node.state.board:
        if square == 0:
            # print(f"{node.state.board} is not terminal")
            return False

    # print(f"{node.state.board} is terminal because no moves are left")
    return True


# Determines value of the board position (for now only determines winners)
# 1 = player 1 wins. -1 = player -1 wins. 0.5 = draw.
def calculate_value(node):
    # print(f"Calculating value of {node.state.board}")
    for row in range(0, 3):
        total = 0
        for col in range(0, 3):
            total += node.state.board[row * 3 + col]
        if total == -3:
            return -1
        elif total == 3:
            return 1
        
    for row in range(0, 3):
        total = 0
        for col in range(0, 3):
            total += node.state.board[row + 3 * col]
        if total == -3:
            return -1
        elif total == 3:
            return 1
    diag1 = node.state.board[0] + node.state.board[4] + node.state.board[8]
    diag2 = node.state.board[2] + node.state.board[4] + node.state.board[6]
    if diag1 == 3 or diag2 == 3:
        return 1
    elif diag1 == -3 or diag2 == -3:
        return -1
    
    # It was a draw
    return 0


# Helper function to print board and make it aesthetically pleasing
def print_board(node):
    for i in range(9):
        if node.state.board[i] == 0:
            print("?", end="")
        elif node.state.board[i] == 1:
            print("X", end="")
        elif node.state.board[i] == -1:
            print("O", end="")

        if i == 2 or i == 5 or i == 8:
            print("")
        else:
            print(" | ", end="")
