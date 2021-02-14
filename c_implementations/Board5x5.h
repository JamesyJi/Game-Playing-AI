#ifndef _MCTSMMAB5X5SBOARD_GUARD
#define _MCTSMMAB5X5SBOARD_GUARD

#include "Structs.h"

#define EMPTY 0
#define PLAYER1 1
#define PLAYER2 -1
#define DRAW 0
#define PLAYER1_WIN 1
#define PLAYER2_WIN -1
#define PLAYER1_CONNECT 4
#define PLAYER2_CONNECT -4
#define NO_LAST_MOVE -1



// Creates a state
State create_state(int *board, int player, int last_move);

// Prints the current state's board
void print_board(State state);

// Populates an array with all possible legal moves
int get_all_possible_moves(State state, int *legal_moves);

// Makes a move on a board
void make_move(State state, int move);

// Undoes a move on a board
void undo_move(State state, int move, int last_move);

// Evaluates a board
int evaluate_position(State state);

// Determines if a position is terminal
int is_terminal(State state);

// Makes a random legal move. Used for simulations
void make_random_move(State state);


// ==========HELPER FUNCTIONS==========

// Finds the largest number in an array
int max_array(int *array, int size);

// Finds the smallest number in an array
int min_array(int *array, int size);

// Frees a state
void free_state(State state);

#endif