import sys
from MinimaxBoard import (
    PLAYER2, State,
)

MAX_INT = float('inf')
MIN_INT = float('-inf')

def make_best_move(state, is_max_player):
    best_move = None
    if is_max_player:
        best_evaluation = MIN_INT
    else:
        best_evaluation = MAX_INT

    for move in state.getAllPossibleMoves():
        state.makeMove(move)
        evaluation = minimax(state, MAX_INT, not is_max_player)
        print(f"best evaluation was {evaluation} with move {move}")
        state.undoMove(move)
        if is_max_player:
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move
        else:
            if evaluation < best_evaluation:
                best_evaluation = evaluation
                best_move = move

    state.makeMove(best_move)
    print(f"Made move with evaluation {evaluation}")
    state.printBoard()

def minimax(state, depth, is_max_player):
    if depth == 0 or state.isTerminal():
        #print(f"Reached terminal state with evaluation {state.evaluatePosition()}")
        #state.printBoard()
        #input()
        return state.evaluatePosition()
    
    if is_max_player:
        max_evaluation = MIN_INT
        eval_list = []
        for move in state.getAllPossibleMoves():
            state.makeMove(move)
            evaluation = minimax(state, depth - 1, False)
            eval_list.append(evaluation)
            state.undoMove(move)
            max_evaluation = max(max_evaluation, evaluation)
        #print(f"Max player evaluation {max_evaluation} from {eval_list}")
        #state.printBoard()
        #input()
        return max_evaluation
    else:
        min_evaluation = MAX_INT
        eval_list = []
        for move in state.getAllPossibleMoves():
            state.makeMove(move)
            evaluation = minimax(state, depth - 1, True)
            eval_list.append(evaluation)
            state.undoMove(move)        
            min_evaluation = min(min_evaluation, evaluation)
        #print(f"Min player evaluation {min_evaluation} from {eval_list}")
        #state.printBoard()
        #input()
        return min_evaluation


if __name__ == "__main__":
    start = State([0, 0, 0, 0, 0, 0, 0, 0, 0], PLAYER2)
    
    is_max_player = True
    while not start.isTerminal():
        make_best_move(start, is_max_player)
        is_max_player = not is_max_player

    print("Game ended like")
    start.printBoard()