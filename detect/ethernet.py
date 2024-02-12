import network
from machine import Pin,SPI
import time
p3v3 = Pin(46, Pin.OUT);p3v3.on();p5v = Pin(45, Pin.OUT);p5v.on()
time.sleep(100)
hspi = SPI(1, 10000000, sck=Pin(1), mosi=Pin(2), miso=Pin(10))
l = network.LAN(phy_addr = 1, phy_type = network.PHY_DM9051,spi=hspi,mdc=Pin(16), mdio=Pin(17))
l.active(True)
print(l.ifconfig())
