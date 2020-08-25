#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "MCTSMMAB5x5S.h"
#include "MCTSMMAB5x5SBoard.h"

// Decides move with MCTS + augments
Node decide_move(Node root_node, time_t time_limit);

int main(void) {
    int start_board[25] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    State start_state = create_state(start_board, PLAYER2, -1);
    Node root_node = create_node(start_state, NULL);

    // Random seed
    srand(time(NULL));

    printf("========================================================\n");
    printf("Starting a new game of tic tac toe. Player 1 moves first\n");
    printf("========================================================\n");
    while (!is_terminal(root_node->state)) {
        //printf("Deciding Move=======================================\n");
        root_node = decide_move(root_node, 1);
        print_board(root_node->state);
        root_node->parent = NULL;
        // getchar();        
    }
    print_board(root_node->state);

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

    /*for (int i = 0; i < root_node->n_children; ++i) {
        print_board(root_node->children[i]->state);
        printf("had value %0.f out of %0.f visits\n", root_node->children[i]->value, root_node->children[i]->visits);
    }*/

    printf("Selected best node with %0.f wins out of %0.f visits\n", best_node->value, best_node->visits);
    return best_node;
}

/* Frees all memory from our tree except for a given child node */
