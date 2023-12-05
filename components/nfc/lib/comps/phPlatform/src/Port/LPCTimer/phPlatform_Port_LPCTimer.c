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
* Platform file to abstract HOST and front-end.
* $Author: Purnank G (ing05193) $
* $Revision: 5450 $ (v4.040.05.011646)
* $Date: 2016-07-06 13:27:31 +0530 (Wed, 06 Jul 2016) $
*
*/

#include <ph_Status.h>
#include <ph_NxpBuild.h>

#if defined (NXPBUILD__PH_LPC11U68) || \
    defined (NXPBUILD__PH_LPC1769)

#include <phPlatform.h>

phStatus_t phPlatform_Port_Host_HwTimer_Init(void)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_Create(uint32_t dwUnits, uint8_t bTimerId, void** ppTimerHandle)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_Configure(void *pTimerHandle, uint32_t dwUnits, uint32_t dwTimePeriod)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_Start(void * pTimerHandle, uint16_t wOption)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_GetElapsedDelay(void * pTimerHandle, uint32_t dwUnits,
        uint32_t *pdwGetElapsedDelay)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_Stop(void * pTimerHandle)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_Reset(void * pTimerHandle)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_Port_Host_HwTimer_Delete(void * pTimerHandle)
{
    return PH_ERR_SUCCESS;
}

void phPlatform_Port_Host_HwTimer_DeInit(void)
{
}

phStatus_t phPlatform_InitTickTimer(pphPlatform_TickTimerISRCallBck_t pTickTimerCallback)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_StartTickTimer(uint32_t dwTimeMilliSecs)
{
    return PH_ERR_SUCCESS;
}

phStatus_t phPlatform_StopTickTimer(void)
{
    return PH_ERR_SUCCESS;
}

/* During FreeRTOS build SysTick_Handler shall be Taken from FreeRTOS port and this API is ignored. */
#ifdef NXPBUILD__PH_OSAL_FREERTOS
/* FreeRTOS would bring it's own SysTick_Handler */
#endif


#endif /* NXPBUILD__PH_LPC11U68 || NXPBUILD__PH_LPC1769 */
/******************************************************************************
**                            End Of File
******************************************************************************/
