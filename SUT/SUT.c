#include "SUT.h"

void compA(int suti0, int suti1, int suti2, int *AO1, int *AO2)
{
    *AO1 = suti0 + suti1;
    *AO2 = suti0 + suti2;
}
void compB(int suit3, int suti4, int suti5, int suti6, int *BO1)
{
    *BO1 = suti4 + suti5 + suti6;
}
void compC(int AO1, int BO1, int *CO1, int *suto2)
{
    *CO1 = AO1 + BO1;
    *suto2 = *CO1;
}
void compD(int CO1, int AO2, int *suto1)
{
    *suto1 = CO1 + AO2;
}

void compE(int *teste)
{
    *teste += 10;
}

void SUT(int suti0, int suti1, int suti2, int suti3, int suti4, int suti5, int suti6, int *suto1, int *suto2)
{
    int AO1, AO2, BO1, CO1;
    compA(suti0, suti1, suti2, &AO1, &AO2);
    compB(suti3, suti4, suti5, suti6, &BO1);
    compC(AO1, BO1, &CO1, suto2);
    compD(CO1, AO2, suto1);
}
