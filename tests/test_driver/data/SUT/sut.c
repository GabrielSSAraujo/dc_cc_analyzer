#include "sut.h"
// Fully covered

void f1(int i1, int *a) {
    *a = i1 * 2;
}

void f2(int a, int *o1) {
    *o1 = a + 3;
}

void sut(int i1, int *o1) {
    int a;
    f1(i1, &a);
    f2(a, o1);
}