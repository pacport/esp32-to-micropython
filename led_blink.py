from machine import Pin, I2C
import time

i2c = I2C(scl=Pin(18),sda=Pin(17),freq=100000)

#print(i2c.scan())
i2c_addr = 32

    
#power on tca9555   
p46 = Pin(46, Pin.OUT)
p46.on()

# set tca9555 port0 to output
i2c.writeto_mem(i2c_addr, 0x06, b'0x00')
while True:
    # turn on power led
    i2c.writeto_mem(i2c_addr, 0x02, b'0x00')
    time.sleep_ms(500)
    
    
    # turn off power led
    i2c.writeto_mem(i2c_addr, 0x02, b'0x01')
    time.sleep_ms(500)




