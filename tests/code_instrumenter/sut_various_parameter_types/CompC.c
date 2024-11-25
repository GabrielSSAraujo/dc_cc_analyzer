/* $*************** KCG Version 6.1.3 (build i6) ****************
** Command: s2c613 -config C:/SW_Tools/Repos/sbx/PES/PES03_SUT_Model/SCADE/KCG\kcg_s2c_config.txt
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

#include "kcg_consts.h"
#include "kcg_sensors.h"
#include "CompC.h"

/* CompC */
kcg_int CompC(/* CompC::CI1 */kcg_real CI1, /* CompC::CI2 */kcg_int CI2)
{
  /* CompC::CO1 */ kcg_int CO1;
  
  CO1 = (kcg_int) CI1 - CI2;
  return CO1;
}

/* $*************** KCG Version 6.1.3 (build i6) ****************
** CompC.c
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

