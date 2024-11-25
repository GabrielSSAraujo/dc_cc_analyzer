#include "../../../../modules/coupling_recorder/coupling_recorder.h"
#include "sut.h"
void f1(int i1, int *a)

{

  *a = i1 * 2;

}



void f2(int a, int *o1)

{

  *o1 = a + 3;

}



void sut(int i1, int *o1)

{

  recorder_setCouplings(3, "a_1", "i1", "o1_1");

  int a;

  recorder_record("i1", &i1, "int");

  f1(i1, &a);

  recorder_record("a_1", &a, "int");

  recorder_record("a_1", &a, "int");

  f2(a, o1);

  recorder_record("o1_1", o1, "int");

}



