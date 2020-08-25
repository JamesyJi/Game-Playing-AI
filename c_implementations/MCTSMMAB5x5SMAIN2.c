/* Implementation for 2 player game */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "MCTSMMAB5x5S.h"
#include "MCTSMMAB5x5SBoard.h"

// Decides move with MCTS + augments
Node decide_move(Node root_node, time_t time_limit);

// Gets new node based on opponent's move
Node update_opponent_move_node(Node root_node);

// Formats output and prints it
void send_output(Node node);

// Pass in arguments: PLAYER_NO, TIME_LIMIT, START_BOARD
int main(int argc, char *argv[]) {
    int player_no = atoi(argv[1]);
    int time_limit = atol(argv[2]);
    int start_board[25];
    for (int i = 3; i <= argc; ++i) {
        start_board[i - 3] = atoi(argv[i]);
    }

    State start_state = create_state(start_board, PLAYER2, NO_LAST_MOVE);
    Node root_node = create_node(start_state, NULL);

    // Random seed
    srand(time(NULL));
    
    // Determines if it is our turn or opponent's turn
    int next_player = PLAYER1;

    while (!is_terminal(root_node->state)) {
        if (next_player == player_no) {
            root_node = decide_move(root_node, time_limit);
            send_output(root_node);
        } else {
            root_node = update_opponent_move_node(root_node);
        }
        next_player = -next_player;
    }

    return 0;
}

/* Decides our move based on implementation logic and then returns the node
we will move into. It wil decide based on the time_limit provided */
Node decide_move(Node root_node, time_t time_limit) {
    time_t start_time = time(NULL);
    time_t end_time = start_time + time_limit;
    while (time(NULL) <= end_time) {
        // SELECTION
        //printf("Selection\n");
        Node promising_node = select_best_child(root_node);

        // print_board(promising_node->state);

        // EXPANSION
        //printf("Expansion\n");
        if (!is_terminal(promising_node->state)) {
            expand_node(promising_node);
        }

        // SIMULATION
        //=printf("Simulation\n");
        Node explore_node;
        if (promising_node->n_children != 0) {
            explore_node = get_random_child(promising_node);
        } else {
            explore_node = promising_node;
        }
        int evaluation = simulate(explore_node);

        // BACK PROPAGATION
        //printf("Back propagation\n");
        back_propagate(explore_node, evaluation);
    }

    // Determine the child with the most visits
    Node best_node = get_most_visited_child(root_node);
    best_node->parent = NULL;
    /*for (int i = 0; i < root_node->n_children; ++i) {
        print_board(root_node->children[i]->state);
        printf("had value %0.f out of %0.f visits\n", root_node->children[i]->value, root_node->children[i]->visits);
    }*/

    printf("Selected best node with %0.f wins out of %0.f visits\n", best_node->value, best_node->visits);
    return best_node;
}

/* Given a node, formats output in PLAYER_NO LAST_MOVE BOARD*/
void send_output(Node node) {
    printf("%d %d", node->state->player, node->state->last_move);
    for (int i = 0; i < 25; ++i) {
        printf(" %d", node->state->board[i]);
    }
    printf("\n");
    return;
}

/* Given a root node (our last turn), scans in opponent's input and then gets the
new node based on their move. If the node does not exist, create it. Return the node. */
Node update_opponent_move_node(Node root_node) {
    // Scan in input
    int last_player, last_move;
    int board[25];
    scanf("%d %d", &last_player, &last_move);
    for (int i = 0; i < 25; ++i) {
        scanf("%d", &board[i]);
    }
    if (root_node->n_children == 0) {
        // Does not exist. we need to create it.
        State state = create_state(board, last_player, last_move);
        Node opponent_move = create_node(state, NULL);
        return opponent_move;
    } else {
        // Exists. Look for it based on last_move
        for (int i = 0; i < root_node->n_children; ++i) {
            if (root_node->children[i]->state->last_move == last_move) {
                root_node->children[i]->parent = NULL;
                return root_node->children[i];
            }
        }
    }
}


/* Frees all memory from our tree except for a given child node */



