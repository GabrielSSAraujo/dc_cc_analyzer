#include "sut.h"

void compA(float suti0, double suti1, int suti2, int *AO1, double *AO2)
{
    *AO1 = (int)(suti0 + suti1);
    *AO2 = suti0 + suti2;
}

void compB(char suti3, int suti4, float suti5, double suti6, float *BO1)
{
    *BO1 = suti3 + suti4 + suti5 + (float)suti6;
}

void compC(int *AO1, float BO1, char *CO1, double *suto2)
{
    *CO1 = (char)(*AO1 + BO1);
    *suto2 = *CO1 + BO1;
}

void compD(char CO1, double AO2, int *suto1)
{
    *suto1 = (int)(CO1 + AO2);
}

int compE(double *eo, int ei)
{
    *eo += ei;
    return (int)*eo;
}

void sut(float suti0, double suti1, int suti2, char suti3, int suti4, float suti5, double suti6, int *suto1, double *suto2)
{
    int ei = 10;
    int a1;        
    double a2;      
    float a3;      
    char a4;       

    compA(suti0, suti1, suti2, &a1, &a2);   
    compB(suti3, suti4, suti5, suti6, &a3); 
    *suto1 = compE(&a2, ei);                
    compC(&a1, a3, &a4, suto2);             
    compD(a4, a2, suto1);                   
}