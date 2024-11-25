#include "sut.h"

void compA(int a, int b, int* d){
    *d = a + b;
}
void compB(int c, int *d, int*e){
    *e = *d + c;
}

void sut(int a,int b,int c,int *d, int *e){
    
    compA(a,b,d);
    compB(c,d,e);
}