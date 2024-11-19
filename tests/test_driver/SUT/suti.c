#include "C:\Users\ALINE\Documents\TCC PES\dc_cc_analyzer-2\modules\coupling_recorder\coupling_recorder.h"
#include "sut.h"
void compA(int SUTI1, int SUTI2, float SUTI3, int *SUTO2, float *SUTO1)

{

  *SUTO1 = SUTI1 + SUTI2;

}



void compB(int SUTI4, int SUTI5, int SUTI6, int *SUTO2)

{

  *SUTO2 = (SUTI4 + SUTI5) + SUTI6;

}



void compC(int *SUTO2, float SUTI3)

{

  *SUTO2 = SUTI3;

}



void compD(float *SUTO1, float SUTI2)

{

  *SUTO1 = SUTI2;

}



void compE(int *teste)

{

  *teste += 10;

}



void sut(int SUTI1, int SUTI2, float SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO2, float *SUTO1)

{

  recorder_setCouplings(3, "SUTO2", "SUTO2_aux", "SUTO1");

  compA(SUTI1, SUTI2, SUTI3, SUTO2, SUTO1);

  recorder_record("SUTO2", SUTO2, "int");

  compB(SUTI4, SUTI5, SUTI6, SUTO2);

  int *SUTO2_aux = SUTO2;

  recorder_record("SUTO2_aux", SUTO2_aux, "int");

  compC(SUTO2, SUTI3);

  recorder_record("SUTO1", SUTO1, "float");

  compD(SUTO1, SUTI2);

}



