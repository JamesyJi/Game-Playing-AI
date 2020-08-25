'''Runs 2 programs against each other'''
import sys
import ctypes
from subprocess import call


if __name__ == "__main__":
    player_a = sys.argv[1] # Program names (Pref to have c program here)
    player_b = sys.argv[2] # Program names
    player1 = int(sys.argv[3]) # 1 = player_a moves first, 2 = player_b moves first
    time_limit = int(sys.argv[5])


    board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    last_player = -1

    if player1 == 1:
        cboard = (ctypes.c_int * len(board))(*board)
        call(sys.argv[1], last_player, time_limit, cboard)
        
    else:



