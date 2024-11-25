#include "/home/gabriel/codes/tcc/dc_cc_analyzer/modules/coupling_recorder/coupling_recorder.h"
#include "sut.h"
void compA(int a, int b, int *d)

{

  *d = a + b;

}



void compB(int c, int *d, int *e)

{

  *e = (*d) + c;

}



void sut(int a, int b, int c, int *d, int *e)

{

  recorder_setCouplings(6, "c", "e_1", "d_2", "d_1", "b", "a");

  recorder_record("a", &a, "int");

  recorder_record("b", &b, "int");

  compA(a, b, d);

  recorder_record("d_1", d, "int");

  recorder_record("c", &c, "int");

  recorder_record("d_1", d, "int");

  compB(c, d, e);

  recorder_record("e_1", e, "int");

  recorder_record("d_2", d, "int");

}



