#ifndef _MCTSMMAB5X5SSTRUCTS_GUARD
#define _MCTSMMAB5X5SSTRUCTS_GUARD

typedef struct State *State;
typedef struct Node *Node;

// Contains information regarding each node
struct Node {
    State state;
    Node parent;
    Node *children;
    int n_possible_children;
    int n_children;
    float value;
    float visits;
};

// Contains information regarding each state
struct State {
    int *board;
    int player;
    int last_move;
};

#endif