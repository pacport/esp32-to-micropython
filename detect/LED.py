from machine import Pin, I2C
import time
import _thread
PORT0_INPUT = 0x00
PORT1_INPUT = 0x01
PORT0_OUTPUT = 0x02
PORT1_OUTPUT = 0x03
PORT0_COMFIG = 0x06
PORT1_COMFIG = 0x07
OUTPUT_MODE = b'\x00'
INPUT_MODE = b'\xff'


CAM_EN = 0x40
PA_CTRL = 0x80

POWE_KEY_LED 	= 0x0100
LED_IR 			= 0x0200
LED_PHOTO		= 0x0400

QR_TRIG			= 0x2000
IO_OUT_USB5V_EN = 0x4000
IO_OUT_MCU_RST	= 0x8000


i2c = None
i2c_addr = 32

def to_byte(integer: int, n=1):
    return integer.to_bytes(n, "big")
def init():
    global i2c
    p3v3 = Pin(46, Pin.OUT)
    p3v3.on()	#power on tca9555  
    i2c = I2C(scl=Pin(18),sda=Pin(17),freq=100000)
  
    # set tca9555 port0 to output
    i2c.writeto_mem(i2c_addr, PORT0_COMFIG, OUTPUT_MODE)
    i2c.writeto_mem(i2c_addr, PORT1_COMFIG, OUTPUT_MODE)
    
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, to_byte(0xff)) # Initial value is 0xff
    i2c.writeto_mem(i2c_addr, PORT1_OUTPUT, to_byte(0x79)) # Initial value is 0x79
    set_led_OFF(leds.NET_LED_RED)
    set_led_ON(leds.NFC_LED_GREEN)
    set_led_OFF(leds.BAT_LED_GREEN)
    

class leds:
    BAT_LED_RED 	= ~0x01
    BAT_LED_GREEN 	= ~0x02
    BAT_LED_ALL		= 0x03

    NET_LED_RED = ~0x04
    NET_LED_GREEN = ~0x08
    NET_LED_ALL	= 0x0c

    NFC_LED_RED = ~0x10
    NFC_LED_GREEN = ~0x20
    NFC_LED_ALL	  = 0x30
    
class status:
    OFF = 0
    ON = 1
def read_PORT0():
    return int.from_bytes(i2c.readfrom_mem(i2c_addr, PORT0_INPUT, 1), "big")


def set_led_ON(led: leds):
    data = read_PORT0()
    i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, to_byte(led & data))
def set_led_OFF(led: leds):
    data = read_PORT0()
    if led == leds.BAT_LED_ALL or led == leds.NET_LED_ALL or led == leds.NFC_LED_ALL:
        i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, to_byte(led | data))
    else:
        i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, to_byte(~led | data))

blinking_bat = False
blinking_net = False
def blink_bat_led(led, arg):
    while blinking_bat == True:
        set_led_OFF(led)
        time.sleep_ms(arg)
        set_led_ON(led)
        time.sleep_ms(arg)
        
def blink_net_led(led, arg):
    while blinking_net == True:
        set_led_OFF(led)
        time.sleep_ms(arg)
        set_led_ON(led)
        time.sleep_ms(arg)
        
def start_blink_led(led: leds):
    global blinking_bat, blinking_net
    if led == leds.BAT_LED_RED or led == leds.BAT_LED_GREEN:
        set_led_OFF(leds.BAT_LED_ALL)
        blinking_bat = True
        _thread.start_new_thread(blink_bat_led, (led, 500))
    elif led == leds.NET_LED_RED or led == leds.NET_LED_GREEN:
        set_led_OFF(leds.NET_LED_ALL)
        blinking_net = True
        _thread.start_new_thread(blink_net_led, (led, 500))

def stop_blink_led(led: leds):
    global blinking_bat, blinking_net
    if led == leds.BAT_LED_RED or led == leds.BAT_LED_GREEN:
        blinking_bat = False
    elif led == leds.NET_LED_RED or led == leds.NET_LED_GREEN:
        blinking_net = False
    
    



