#include "/home/bruno/dc_cc_analyzer/modules/coupling_recorder/coupling_recorder.h"
#include <stdio.h>
#include "sut.h"
int f1(int i1, float i2)

{

  int a;

  a = ((int) i2) + i1;

  return a;

}



void f2(float i2, float *b, float *h)

{

  *h = 2 * i2;

  if ((*h) > 3)

  {

    *b = *h;

  }

  else

  {

    *b = -1;

  }

}



void f3(float i2, int i3, float *h, int *e, float *g)

{

  int aux1;

  float aux2;

  aux1 = ((int) i2) + i3;

  aux2 = i2 - ((float) i3);

  *e = aux1;

  if ((i2 < 0) && (i3 == 1000))

  {

    *g = aux2 + (*h);

  }

  else

  {

    *g = 20.1;

  }

}



float f4(int a, float *b)

{

  return (*b) + 0.1;

}



void f5(float *b, int e, float d, float *f, int *o2)

{

  if ((*b) < 0)

  {

    *o2 = e;

    *f = d;

  }

  else

  {

    *o2 = 1;

    *f = (float) e;

  }

}



int f6(float *c, float *d)

{

  int o1 = 0;

  *d = (*c) - 20;

  if ((*d) > 100)

  {

    o1 = (*d) - 100;

  }

  return o1;

}



float f7(float f, float *g)

{

  float o3;

  float aux;

  aux = f * (*g);

  o3 = aux - 50;

  return o3;

}



void sut(int i1, float i2, int i3, int *o1, int *o2, float *o3)

{

  recorder_setCouplings(19, "d_1", "e_1", "c", "o3", "f_1", "h_2", "b_3", "o1", "a", "b_1", "h_1", "b_2", "i2", "g_1", "c_1", "g_2", "i3", "i1", "o2_1");

  int a;

  int e;

  float b;

  float c;

  float d;

  float f;

  float g;

  float h;

  recorder_record("i1", &i1, "int");

  recorder_record("i2", &i2, "float");

  a = f1(i1, i2);

  recorder_record("a", &a, "int");

  recorder_record("i2", &i2, "float");

  f2(i2, &b, &h);

  recorder_record("h_1", &h, "float");

  recorder_record("b_1", &b, "float");

  recorder_record("i2", &i2, "float");

  recorder_record("i3", &i3, "int");

  recorder_record("h_1", &h, "float");

  f3(i2, i3, &h, &e, &g);

  recorder_record("g_1", &g, "float");

  recorder_record("e_1", &e, "int");

  recorder_record("h_2", &h, "float");

  recorder_record("a", &a, "int");

  recorder_record("b_1", &b, "float");

  c = f4(a, &b);

  recorder_record("b_2", &b, "float");

  recorder_record("c", &c, "float");

  recorder_record("c", &c, "float");

  *o1 = f6(&c, &d);

  recorder_record("d_1", &d, "float");

  recorder_record("c_1", &c, "float");

  recorder_record("o1", o1, "int");

  recorder_record("b_2", &b, "float");

  recorder_record("e_1", &e, "int");

  recorder_record("d_1", &d, "float");

  f5(&b, e, d, &f, o2);

  recorder_record("o2_1", o2, "int");

  recorder_record("f_1", &f, "float");

  recorder_record("b_3", &b, "float");

  recorder_record("f_1", &f, "float");

  recorder_record("g_1", &g, "float");

  *o3 = f7(f, &g);

  recorder_record("g_2", &g, "float");

  recorder_record("o3", o3, "float");

}



