#include "sut.h"

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

void sut(int suti0, int suti1, int suti2, int suti3, int suti4, int suti5, int suti6, int *suto1, int *suto2, int *suto3, int *suto4, int *suto5, int *suto6)
{
    int teste;
    int *teste2;
    //int AO1, AO2, BO1, CO1;
    compA(suti0, suti1, suti2, suto1, suto2);
    compB(suti3, suti4, suti5, suti6, suto3);
    compC(*suto1, *suto3, suto4, suto2);
    compD(*suto4, *suto2, suto1);
}
