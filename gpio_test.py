from machine import Pin, I2C
import time

i2c = I2C(0)

addr = 0x22

GPIO0_CMD = int(0x06).to_bytes(1, 'big')
GPIO1_CMD = int(0x07).to_bytes(1, 'big')

def write_one_byte(addr, cmd, data):
    i2c.writeto(addr, cmd)
    i2c.writeto(addr, data.to_bytes(1, 'big'))


while True:
    write_one_byte(addr, GPIO0_CMD, 0x00)
    write_one_byte(addr, GPIO1_CMD, 0x00)
    time.sleep_ms(500)
    
    
    write_one_byte(addr, GPIO0_CMD, 0xff)
    write_one_byte(addr, GPIO1_CMD, 0xff)
    time.sleep_ms(500)