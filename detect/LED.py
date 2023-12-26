from machine import Pin, I2C
import time
PORT0_INPUT = 0x00
PORT1_INPUT = 0x01
PORT0_OUTPUT = 0x02
PORT1_OUTPUT = 0x03
PORT0_COMFIG = 0x06
PORT1_COMFIG = 0x07
OUTPUT_MODE = b'0x00'
INPUT_MODE = b'0xff'

POWER_BUTTON_LED = 	b'0x01' # off
BACK_CAM1_LED 	= 	b'0x02' # on
BACK_CAM2_LED 	= 	b'0x04' # on
i2c = None
i2c_addr = 32


def init():
    global i2c
    p3v3 = Pin(46, Pin.OUT)
    p3v3.on()	#power on tca9555  
    i2c = I2C(scl=Pin(18),sda=Pin(17),freq=100000)
  
    # set tca9555 port0 to output
    i2c.writeto_mem(i2c_addr, PORT0_COMFIG, OUTPUT_MODE)
    i2c.writeto_mem(i2c_addr, PORT1_COMFIG, OUTPUT_MODE)
    while True:
        i2c.writeto_mem(i2c_addr, PORT1_OUTPUT, b'0x00')
        time.sleep_ms(500)
        i2c.writeto_mem(i2c_addr, PORT1_OUTPUT, b'0x80')
        time.sleep_ms(500)
#init()  
def set0():
    data = None
    i2c.readfrom_mem(i2c_addr, PORT0_INPUT, data)
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, b'0x00')


def read_PORT0():
    return i2c.readfrom_mem(i2c_addr, PORT0_INPUT, 1)

def set_bat_led_red():
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, b'0x20')
    
def set_bat_led_greed():
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, b'0x10')
    
def set_net_led_green():
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, b'0x40')
def set_net_led_red():
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, b'0x80')




