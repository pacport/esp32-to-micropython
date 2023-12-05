/*
*         Copyright (c), NXP Semiconductors Bangalore / India
*
*                     (C)NXP Semiconductors
*       All rights are reserved. Reproduction in whole or in part is
*      prohibited without the written consent of the copyright owner.
*  NXP reserves the right to make changes without notice at any time.
* NXP makes no warranty, expressed, implied or statutory, including but
* not limited to any implied warranty of merchantability or fitness for any
*particular purpose, or that the use will not infringe any third party patent,
* copyright or trademark. NXP must not be liable for any loss or damage
*                          arising from its use.
*/

/** \file
* Platform file abstracting HOST features.
* $Author: Ankur Srivastava (nxp79569) $
* $Revision: 5812 $ (v4.040.05.011646)
* $Date: 2016-08-30 20:13:02 +0530 (Tue, 30 Aug 2016) $
*
*/

#include <ph_Status.h>

#ifdef NXPBUILD__PH_LPC1769

#include <phPlatform.h>
#include <phPlatform_Port_Host.h>

void phPlatform_EnterCriticalSection(void)
{

}

void phPlatform_ExitCriticalSection(void)
{

}

uint32_t phPlatform_Is_Irq_Context(void)
{
    return 0;
}

void phPlatform_Sleep(void)
{

}

void phPlatform_WakeUp(void)
{

}

void phPlatform_Controller_Init(void)
{
	return ;
}

phStatus_t phPlatform_Port_Host_SetPinConfig(phPlatform_Port_Host_config_t bConfig)
{
    return PH_ERR_SUCCESS;
}

void phPlatform_Port_Host_SetPinValue(phPlatform_Port_Host_config_t bConfig, uint8_t bVal)
{
}

bool phPlatform_Port_Host_GetPinValue(phPlatform_Port_Host_config_t bConfig)
{
    bool    bStatus = false;
    return bStatus;
}

void phPlatform_Port_Host_ClearInt()
{

}

#endif /* NXPBUILD__PH_LPC1769 */
