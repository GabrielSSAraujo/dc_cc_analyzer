#include "/home/bruno/dc_cc_analyzer/modules/coupling_recorder/coupling_recorder.h"
void f1(int i1, int *a)

{

  *a = i1 * 2;

}



void f2(int a, int *o1)

{

  *o1 = a + 3;

}



int f3()

{

  return 10;

}



void sut(int i1, int *o1)

{

  recorder_setCouplings(4, "i1", "a_1", "o1_1", "a_2");

  int a;

  recorder_record("i1", &i1, "int");

  f1(i1, &a);

  recorder_record("a_1", &a, "int");

  a = f3();

  recorder_record("a_2", &a, "int");

  recorder_record("a_2", &a, "int");

  f2(a, o1);

  recorder_record("o1_1", o1, "int");

}



