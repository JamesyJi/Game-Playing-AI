
#include <stdio.h>
#include <stdlib.h>

#include "MCTSMMAB5x5SBoard.h"


/* Creates and returns a State struct given a board, player who moved into this
state, and last move made by that player. */
State create_state(int *board, int player, int last_move) {
    State new = malloc(sizeof (struct State));
    new->board = (int *) calloc(25, sizeof(int));
    for (int i = 0; i < 25; ++i) {
        new->board[i] = board[i];
    }
    new->player = player;
    new->last_move = last_move;

    return new;
}


/* Given a state, prints the board */
void print_board(State state) {
    for (int i = 0; i < 25; ++i) {
        // printf("Square is %d\n", state->board[i]);
        if (state->board[i] == EMPTY) {
            printf(" ? ");
        } else if (state->board[i] == PLAYER1) {
            printf("\033[0;34m");
            printf(" X ");
            printf("\033[0m");
        } else {
            printf("\033[0;31m");
            printf(" O ");
            printf("\033[0m");
        }

        if ((i + 1) % 5 == 0) {
            printf("\n");
        } else {
            printf(" | ");
        }
    }

    return;
}


/* Finds all possible legal moves and populates the given array with them. Also
returns the number of moves found */
int get_all_possible_moves(State state, int *legal_moves) {
    int n_moves = 0;

    for (int move = 0; move < 25; ++move) {
        if (state->board[move] == EMPTY) {
            legal_moves[n_moves] = move;
            n_moves++;
        }
    }
    return n_moves;
}

/* Given a state and a move, makes that move on the board. Toggles the player
and updates the last move */
void make_move(State state, int move) {
    state->player = -state->player;
    state->board[move] = state->player;
    state->last_move = move;
    return;
}

/* Given a state, a move and the last_move prior, undoes the move and "resets"
the state to its prior conditions one move ago */
void undo_move(State state, int move, int last_move) {
    state->player = -state->player;
    state->board[move] = EMPTY;
    state->last_move = last_move;
    return;
}

/* Given a state, evaluates the position of the board and returns it.
Note that only the last player to have moved can win (you cannot "suicide"). */
int evaluate_position(State state) {
    if (state->last_move == NO_LAST_MOVE) {
        return DRAW;
    }

    // Get's the row (multiple of 5) and the column of the last move
    int last_col = state->last_move % 5;
    int last_row = state->last_move - last_col;

    // Checks if the row or column was won by the player who just moved
    int row_col_wins[4];
    row_col_wins[0] = state->board[last_row] + state->board[last_row + 1] + state->board[last_row + 2] + state->board[last_row + 3];
    row_col_wins[1] = state->board[last_row + 1] + state->board[last_row + 2] + state->board[last_row + 3] + state->board[last_row + 4];
    row_col_wins[2] = state->board[last_col] + state->board[last_col + 5] + state->board[last_col + 10] + state->board[last_col + 15];
    row_col_wins[3] = state->board[last_col + 5] + state->board[last_col + 10] + state->board[last_col + 15] + state->board[last_col + 20];

    if (max_array(row_col_wins, 4) == PLAYER1_CONNECT) {
        return PLAYER1_WIN;
    } else if (min_array(row_col_wins, 4) == PLAYER2_CONNECT) {
        return PLAYER2_WIN;
    }

    int diagonals[8];
    diagonals[0] = state->board[0] + state->board[6] + state->board[12] + state->board[18];
    diagonals[1] = state->board[6] + state->board[12] + state->board[18] + state->board[24];
    diagonals[2] = state->board[4] + state->board[8] + state->board[12] + state->board[16];
    diagonals[3] = state->board[8] + state->board[12] + state->board[16] + state->board[20];
    diagonals[4] = state->board[1] + state->board[7] + state->board[13] + state->board[19];
    diagonals[5] = state->board[5] + state->board[11] + state->board[17] + state->board[23];
    diagonals[6] = state->board[3] + state->board[7] + state->board[11] + state->board[15];
    diagonals[7] = state->board[9] + state->board[13] + state->board[17] + state->board[21];
    
    if (max_array(diagonals, 8) == PLAYER1_CONNECT) {
        return PLAYER1_WIN;
    } else if (min_array(diagonals, 8) == PLAYER2_CONNECT) {
        return PLAYER2_WIN;
    }

    return DRAW;
}

/* Given a state, returns 1 if a position is terminal and 0 if not */
int is_terminal(State state) {
    if (evaluate_position(state) != DRAW) {
        return 1;
    }

    for (int i = 0; i < 25; ++i) {
        if (state->board[i] == EMPTY) {
            return 0;
        }
    }

    return 1;
}

/* Given a state, makes a random legal move and toggles the player */
void make_random_move(State state) {
    state->player = -state->player;

    // Find all legal moves
    int legal_moves[25];
    int n_moves = get_all_possible_moves(state, legal_moves);
    
    // Randomly selects move and updates state
    
    int move = legal_moves[rand() % n_moves];
    state->board[move] = state->player;
    state->last_move = move;

    return;
}


// ==========HELPER FUNCTIONS==========

/* Given an array and its size, returns the largest number */
int max_array(int *array, int size) {
    int max_element = array[0];
    for (int i = 1; i < size; ++i) {
        if (array[i] > max_element) {
            max_element = array[i];
        }
    }
    return max_element;
}

/* Given an array and its size, returns the smallest number */
int min_array(int *array, int size) {
    int min_element = array[0];
    for (int i = 1; i < size; ++i) {
        if (array[i] < min_element) {
            min_element = array[i];
        }
    }
    return min_element;
}

/* Given a state, frees all memory allocated to it */
void free_state(State state) {
    free(state->board);
    free(state);
    return;
}