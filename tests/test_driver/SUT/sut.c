
#include "sut.h"

void compA(int SUTI1, int SUTI2, float SUTI3, int *SUTO2, float * SUTO1)
{
    *SUTO1 = SUTI1 + SUTI2;
}
void compB(int SUTI4, int SUTI5, int SUTI6, int *SUTO2)
{
    *SUTO2 = SUTI4 + SUTI5 + SUTI6;
}
void compC(int * SUTO2, float SUTI3)
{
    *SUTO2 = SUTI3;

}
void compD(float * SUTO1, float SUTI2)
{
    *SUTO1 = SUTI2;
}

void compE(int *teste)
{
    *teste += 10;
}

void sut(int SUTI1, int SUTI2, float SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO2, float *SUTO1)
{
    //int AO1, AO2, BO1, CO1;
    compA(SUTI1, SUTI2, SUTI3, SUTO2, SUTO1);
    compB(SUTI4, SUTI5, SUTI6, SUTO2);
    compC(SUTO2,  SUTI3);
    compD(SUTO1, SUTI2);
}
