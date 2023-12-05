/*
 * This file is part of the OpenMV project.
 * Copyright (c) 2013/2014 Ibrahim Abdelkader <i.abdalkader@gmail.com>
 * This work is licensed under the MIT license, see the file LICENSE for details.
 *
 * SCCB (I2C like) driver.
 *
 */
#ifndef __SCCB_H__
#define __SCCB_H__
#include <stdint.h>

typedef void (*sccb_lock_cbr)(int lock);

int SCCB_Init(int pin_sda, int pin_scl, sccb_lock_cbr cbr);
int SCCB_Use_Port(int sccb_i2c_port, sccb_lock_cbr cbr);
int SCCB_Deinit(void);
uint8_t SCCB_Probe();
uint8_t SCCB_Read(uint8_t slv_addr, uint8_t reg);
uint8_t SCCB_Write(uint8_t slv_addr, uint8_t reg, uint8_t data);
uint8_t SCCB_Read16(uint8_t slv_addr, uint16_t reg);
uint8_t SCCB_Write16(uint8_t slv_addr, uint16_t reg, uint8_t data);
#endif // __SCCB_H__
