/* $*************** KCG Version 6.1.3 (build i6) ****************
** Command: s2c613 -config C:/SW_Tools/Repos/sbx/PES/PES03_SUT_Model/SCADE/KCG\kcg_s2c_config.txt
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

#include "kcg_consts.h"
#include "kcg_sensors.h"
#include "CompA.h"

/* CompA */
void CompA(
  /* CompA::AI1 */kcg_bool AI1,
  /* CompA::AI2 */kcg_real AI2,
  /* CompA::AI3 */kcg_real AI3,
  /* CompA::AO1 */kcg_real *AO1,
  /* CompA::AO2 */kcg_real *AO2)
{
  if (AI1) {
    *AO1 = AI2;
  }
  else {
    *AO1 = AI3;
  }
  *AO2 = *AO1 * 2.0;
}

/* $*************** KCG Version 6.1.3 (build i6) ****************
** CompA.c
** Generation date: 2024-09-17T13:38:57
*************************************************************$ */

