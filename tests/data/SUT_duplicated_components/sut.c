#include "sut.h"

void compA(float suti0, double suti1, int suti2, int *AO1, double *AO2)
{
    *AO1 = (int)(suti0 + suti1);
    *AO2 = suti0 + suti2;
}

void compB(char suit3, int suti4, float suti5, double suti6, float *BO1)
{
    *BO1 = suit3 + suti4 + suti5 + (float)suti6;
}

double* compC(int AO1, float BO1, double *CO1, double *suto2)
{
    *CO1 = AO1 + BO1;
    *suto2 = *CO1;
    return *CO1*3;
}

void compD(double CO1, double AO2, int *suto1)
{
    *suto1 = (int)(CO1 + AO2);
}

void compE(double *eo, int ei)
{
    *eo += ei;
}

void sut(float suti0, double suti1, int suti2, char suti3, int suti4, float suti5, double suti6, int *suto1, double *suto2, float *suto3, char *suto4, int *suto5, double *suto6)
{
    int ei = 10;
    double result;

    compA(suti0, suti1, suti2, suto1, suto2);
    compB(suti3, suti4, suti5, suti6, suto3);
    compE(suto2, ei);
    compA(suti5, *sut2, suti2, suto1, suto2);
    result = compC(*suto1, *suto3, suto6, suto2);
    compD(result, *suto2, suto1);
}
