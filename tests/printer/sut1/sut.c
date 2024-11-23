/* This source code is intended to exercise the DC/CC tool developed by Embraer PES3 */
/* Author: jdavison */
/* Revision 0.3 (Nov 04, 2024)*/

#include <stdio.h>
#include "sut.h"

/* ---------------- Software components: f1, f2, f3... ------------*/
int f1(int i1, float i2){
    int a;
    a = (int)i2 + i1;
    return a;
}

void f2(float i2,   float *b, float *h){
    *h = 2 * i2;
    if(*h > 3){
        *b = *h;
    }
    else{
        *b = -1;
    }
}

void f3(float i2, int i3, float *h,   int *e, float *g){
    int aux1;
    float aux2;
    aux1 = (int)i2 + i3;
    aux2 = i2 - (float)i3;

    *e = aux1;
    if((i2 < 0) && (i3 == 1000)){
        *g = aux2 + *h;
    }
    else{
        *g = 20.1;
    }
}

float f4(int a, float *b){
    return *b + 0.1;
}

void f5(float *b, int e, float d,   float *f, int *o2){

    if(*b < 0){
        *o2 = e;
        *f = d;
    }
    else{
        *o2 = 1;
        *f = (float)e;
    }
}

int f6(float *c, float *d){
    int o1 = 0;
    *d = *c - 20;
    if(*d > 100){
        o1 = *d - 100; 
    }
    return o1;
}

float f7(float f, float *g){
    float o3, aux;
    aux = f * (*g);

    o3 = aux - 50; 
    return o3;
}

/* ---------------------------- The SUT! ----------------------------*/
void sut(int i1, float i2, int i3,   int *o1, int *o2, float *o3){
    int a, e; 
    float b, c, d, f, g, h;

    a = f1(i1, i2);
    f2(i2, &b, &h);
    f3(i2, i3, &h, &e, &g);
    c = f4(a, &b);
    *o1 =f6(&c, &d);
    f5(&b, e, d, &f, o2);
    *o3 = f7(f, &g);
}
/* ---------------------------- end SUT ----------------------------*/

