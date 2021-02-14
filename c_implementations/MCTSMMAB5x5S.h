#ifndef _MCTSMMAB5X5S_GUARD
#define _MCTSMMAB5X5S_GUARD

#include "Structs.h"

// Creates a node
Node create_node(State state, Node parent);

// Frees a node
void free_node(Node node);

// Selects the most promising node to explore
Node select_best_child(Node node);

// Expands a node, creating children nodes
void expand_node(Node node);

// Simulates node and evaluates
int simulate(Node node);

// Minimax check for forced wins/losses
int minimax(State state, int depth, int alpha, int beta, int player);

// Rollout policy dictates how we run our simulations
void rollout_policy(State state);

// Backpropagates values
void back_propagate(Node node, int evaluation);

// Gets a random child from a node
Node get_random_child(Node node);

// Gets the child with the most visits
Node get_most_visited_child(Node node);

// Frees a node and all its children except for a given child node
void free_all_other_nodes(Node node, Node child);

#endif