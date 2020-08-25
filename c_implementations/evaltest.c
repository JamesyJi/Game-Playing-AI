#include <assert.h>
#include <stdio.h>

#include "MCTSMMAB5x5SBoard.h"

int main(void) {
    printf("==========Testing evaluation of 5x5 board==========\n");

    int board1[25] = {1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    State s1 = create_state(board1, 1, 3);
    assert(evaluate_position(s1) == 1);

    int board2[25] = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    State s2 = create_state(board2, 1, 0);
    assert(evaluate_position(s2) == 1);

    int board3[25] = {1, 0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, -1, -1, 0, 1, 1, 1, -1, 0, 0, 0, 0, -1, 0};
    State s3 = create_state(board3, -1, 18);
    printf("%d\n", evaluate_position(s3));
    assert(evaluate_position(s3) == -1);

    return 0;
}