/* $*************** KCG Version 6.1.3 (build i6) ****************
** Command: s2c613 -config C:/SW_Tools/Repos/sbx/PES/PES03_SUT_Model/SCADE/KCG\kcg_s2c_config.txt
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

#include "kcg_consts.h"
#include "kcg_sensors.h"
#include "CompB.h"

/* CompB */
kcg_int CompB(
  /* CompB::BI1 */kcg_int BI1,
  /* CompB::BI2 */kcg_int BI2,
  /* CompB::BI3 */kcg_int BI3,
  /* CompB::BI4 */kcg_int BI4)
{
  /* CompB::BO1 */ kcg_int BO1;
  
  BO1 = BI1 + BI2 + BI3 + BI4;
  return BO1;
}

/* $*************** KCG Version 6.1.3 (build i6) ****************
** CompB.c
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

