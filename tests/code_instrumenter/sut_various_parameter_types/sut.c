/* $*************** KCG Version 6.1.3 (build i6) ****************
** Command: s2c613 -config C:/SW_Tools/Repos/sbx/PES/PES03_SUT_Model/SCADE/KCG\kcg_s2c_config.txt
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

#include "kcg_consts.h"
#include "kcg_sensors.h"
#include "sut.h"

/* SUT */
void sut(kcg_bool /* SUT::SUTI1 */ SUTI1,
  kcg_real /* SUT::SUTI2 */ SUTI2,
  kcg_real /* SUT::SUTI3 */ SUTI3,
  kcg_int /* SUT::SUTI4 */ SUTI4,
  kcg_int /* SUT::SUTI5 */ SUTI5,
  kcg_int /* SUT::SUTI6 */ SUTI6,
  kcg_int /* SUT::SUTI7 */ SUTI7, 
  kcg_real /* SUT::SUTO1 */ *SUTO1,
  kcg_int /* SUT::SUTO2 */ *SUTO2)
{
  kcg_int tmp;
  /* SUT::L1 */ kcg_real L1;
  /* SUT::L2 */ kcg_real L2;
  
  /* 1 */ CompA(SUTI1, SUTI2, SUTI3, &L1, &L2);
  tmp = /* 1 */ CompB(SUTI4, SUTI5,SUTI6, SUTI7);
  *SUTO2 = /* 1 */ CompC(L1, tmp);
  *SUTO1 = /* 1 */ CompD(*SUTO2, L2);
}

/* $*************** KCG Version 6.1.3 (build i6) ****************
** SUT.c
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

