#include <stdio.h>
#include <stdlib.h>
#include "SUT.h"

#define ROWS 3
#define COLS 7

#define OUT_COLS 2

int main()
{
    /*init data*/
    int test_data[ROWS][COLS] = {{1, 2, 3, 4, 5, 6, 7},
                                 {7, 6, 5, 4, 3, 2, 1},
                                 {7, 6, 5, 3, 1, 2, 4}};

    int validator[ROWS][OUT_COLS] = {{25, 21},
                                     {21, 29},
                                     {32, 20}};
    /*end data */

    int out1,
        out2;

    for (int i = 0; i < ROWS; i++)
    {
        SUT(test_data[i][0], test_data[i][1], test_data[i][2],
            test_data[i][3], test_data[i][4], test_data[i][5],
            test_data[i][6], &out1, &out2);

        if (out1 == validator[i][0] && out2 == validator[i][1])
            printf("PASS\n");
        else
            printf("FAIL\n");
    }

    return 0;
}