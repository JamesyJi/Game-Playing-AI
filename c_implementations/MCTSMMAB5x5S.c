#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h> 
#include <math.h>

#include "MCTSMMAB5x5SBoard.h"
#include "MCTSMMAB5x5S.h"

static int n_legal_moves(State state);
static float calculate_score(Node node);

/* Given a state, parent, creates a new node */
Node create_node(State state, Node parent) {
    Node new = malloc(sizeof (struct Node));
    new->state = state;
    new->parent = parent;

    // Determine the number of possible children
    int n_possible_children = n_legal_moves(state);
    new->children = malloc(n_possible_children * sizeof (struct Node*));
    for (int i = 0; i < n_possible_children; ++i) {
        new->children[i] = malloc(sizeof(struct Node));
    }
    new->n_possible_children = n_possible_children;
    new->n_children = 0;
    new->value = 0;
    new->visits = 0;

    return new;
}

/* Given a node, SELECTS the child with the highest UCT score until we reach
a leaf node and then return it */
Node select_best_child(Node node) {
    Node best_child = node;
    
    while (1) {
        // printf("Hi %d\n", best_child->n_children);
        if (best_child->n_children == 0) {
            // printf("Returning\n");
            return best_child;
        }

        // Find the child with the highest score
        float best_score = calculate_score(best_child->children[0]);
        //printf("Best_score is %f\n", best_score);
        int max_child = 0;
        for (int i = 0; i < best_child->n_children; ++i) {
            float score = calculate_score(best_child->children[i]);            
            //printf("Child %d has score %f\n", i, score);
            if (score > best_score) {
                best_score = score;
                max_child = i;
                //printf("%d\n", max_child);
            }
        }

        // Assign best child
        //printf("Max_child was %d\n", max_child);
        best_child = best_child->children[max_child];
        // print_board(best_child->state);
    }
}

/* Given a node, EXPANDS determines all possible states (legal positions 
achievable in one move) and adds them to the node's as children */
void expand_node(Node node) {
    // printf("Expanding=================================\n");
    // print_board(node->state);
    int opponent = -node->state->player;
    int new_children = 0;
    for (int move = 0; move < 25; ++move) {
        if (node->state->board[move] == EMPTY) {
            int new_board[25];
            memcpy(new_board, node->state->board, sizeof(new_board));
            new_board[move] = opponent;
            // printf("Newboard move %d %d\n", move, new_board[move]);
            State new_state = create_state(new_board, opponent, move);
            Node child = create_node(new_state, node);
            node->children[new_children] = child;
            new_children++;
        }
    }

    node->n_children = new_children;
    /*printf("EXPANSION CHECK\n");
    for (int i = 0; i < node->n_children; ++i) {
        print_board(node->children[i]->state);
        printf("=================================\n");
    }*/
    return;
}

/* Runs a simulation on a node based on our rollout policy.
Returns the evaluation of the position */
int simulate(Node node) {
    //printf("SIMULATING\n");
    //print_board(node->state);
    //getchar();
    // Creates a new state to be used in simulation
    State simulate_state = create_state(node->state->board, node->state->player, node->state->last_move);
    
    while (!is_terminal(simulate_state)) {
        rollout_policy(simulate_state);
    }

    int evaluation = evaluate_position(simulate_state);
    free(simulate_state);
    return evaluation;
}

/* Rollout policy determines how we run our simulations. This is currently
on a random playout */
void rollout_policy(State state) {
    make_random_move(state);
    return;
}

/* Back propagates the evaluation until the root */
void back_propagate(Node node, int evaluation) {
    Node current = node;
    while (current->parent != NULL) {
        if (current->state->player == evaluation) {
            current->value++; // This player won
        } else if (current->state->player == -evaluation) {
            current->value--; // This player lost
        }
        current->visits++;
        current = current->parent;
    }

    return;
}

/* Given a node with children, returns a random child */
Node get_random_child(Node node) {
    int child = rand() % node->n_children;

    return node->children[child];
}

/* Given a node with children, returns child with the most visits */
Node get_most_visited_child(Node node) {
    int most_child = 0;
    int n_visits = node->children[0]->visits;

    for (int i = 0; i < node->n_children; ++i) {
        if (node->children[i]->visits > n_visits) {
            n_visits = node->children[i]->visits;
            most_child = i;
        }
    }

    return node->children[most_child];
}

// ==========HELPER FUNCTIONS==========

/* Returns the number of legal moves from a given state */
static int n_legal_moves(State state) {
    int n = 0;
    for (int i = 0; i < 25; ++i) {
        if (state->board[i] == EMPTY) {
            n++;
        }
    }
    return n;
}

/* Calculates the UCT score of a node and returns it as a float (faster) */
static float calculate_score(Node node) {
    float score = node->value/(node->visits + 1) + 1.41 * sqrt(log(node->parent->visits/node->visits + 1));
    return score;
}