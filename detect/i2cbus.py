from machine import Pin, I2C

class i2cbus:
    def __init__(self):
        self.i2c = I2C(1, scl=Pin(18),sda=Pin(17),freq=400000)
        print("i2cbus init OK")
    def writeto_mem(self, addr, memaddr, data ):
        return self.i2c.writeto_mem(addr, memaddr, data.to_bytes(1, "big"))

    def readfrom_mem(self, addr, memaddr, n ):
        data = self.i2c.readfrom_mem(addr, memaddr, n)
        data = int.from_bytes(data, 'big')
        return data
        
i2c = i2cbus() 
    
        

