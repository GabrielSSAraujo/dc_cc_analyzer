/* $*************** KCG Version 6.1.3 (build i6) ****************
** Command: s2c613 -config C:/SW_Tools/Repos/sbx/PES/PES03_SUT_Model/SCADE/KCG\kcg_s2c_config.txt
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

#include "kcg_consts.h"
#include "kcg_sensors.h"
#include "CompD.h"

/* CompD */
kcg_real CompD(/* CompD::DI1 */kcg_int DI1, /* CompD::DI2 */kcg_real DI2)
{
  /* CompD::DO1 */ kcg_real DO1;
  
  DO1 = (kcg_real) DI1 + DI2;
  return DO1;
}

/* $*************** KCG Version 6.1.3 (build i6) ****************
** CompD.c
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

