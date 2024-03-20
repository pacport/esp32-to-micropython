from machine import Pin
import time
import _thread
from i2cbus import i2c

PORT0_INPUT = 0x00
PORT1_INPUT = 0x01
PORT0_OUTPUT = 0x02
PORT1_OUTPUT = 0x03
PORT0_COMFIG = 0x06
PORT1_COMFIG = 0x07
OUTPUT_MODE = 0x00
INPUT_MODE = 0xff

BAT_LED_RED = 	0x01
BAT_LED_GREEN = 0x02
NET_LED_RED = 	0x04
NET_LED_GREEN = 0x08
NFC_LED_RED = 	0x10
NFC_LED_GREEN = 0x20
CAM_EN = 		0x40
PA_CTRL = 		0x80
POWE_KEY_LED = 	0x0100
LED_IR 	= 		0x0200
LED_PHOTO	= 	0x0400

QR_TRIG		= 	0x2000
USB5V_EN 	= 	0x4000
MCU_RST		= 	0x8000






class TCA9555:
    tac9555_i2c_addr = 32 #0x20
    def __init__(self):
        p3v3 = Pin(46, Pin.OUT)
        p3v3.on()
        time.sleep_ms(10)
        # set tca9555 port0 to output
        self.__write_port(PORT0_COMFIG, OUTPUT_MODE)
        self.__write_port(PORT1_COMFIG, OUTPUT_MODE)
        self.__write_port(PORT0_OUTPUT, 0xff) # Initial value is 0xff
        self.__write_port(PORT1_OUTPUT, 0x79) # Initial value is 0x79
        print('tca9555 inited')
        
    def __read_PORT(self, port_num):
        if port_num == PORT0_INPUT or port_num == PORT1_INPUT:
            return i2c.readfrom_mem(self.tac9555_i2c_addr, port_num, 1)
        return None
    def __write_port(self, port_num, data):
        if port_num >= PORT0_INPUT and port_num <= PORT1_COMFIG:
            return i2c.writeto_mem(self.tac9555_i2c_addr, port_num, data)
        return None
    def set_gpio(self, pins, status):
        if pins <= 0xff: #pins in PORT0
            port = PORT0_OUTPUT
            read_port = PORT0_INPUT
        elif pins > 0xff and  pins <= 0xffff:
            port = PORT1_OUTPUT
            pins = pins >> 8
            read_port = PORT1_INPUT
        data = self.__read_PORT(read_port)
        if status == 1:
            data = data | pins
        else:
            pins = ~pins
            data = data & pins
        self.__write_port(port, data)
            
tca9555 = TCA9555()

net_led_blink = None

def blink_net_led_red():
    
    tca9555.set_gpio(NET_LED_GREEN, 1)
    state = 1
    while net_led_blink == NET_LED_RED:
        state = ~state
        tca9555.set_gpio(NET_LED_RED, state)
        time.sleep_ms(300)

def blink_net_led_green():
    tca9555.set_gpio(NET_LED_RED, 1)
    state = 1
    while net_led_blink == NET_LED_GREEN:
        state = ~state
        tca9555.set_gpio(NET_LED_GREEN, state)
        time.sleep_ms(300)

def blink_NET_LED_RED():
    global net_led_blink
    net_led_blink = NET_LED_RED
    _thread.start_new_thread(blink_net_led_red, ())
    

def blink_NET_LED_GREEN():
    global net_led_blink
    net_led_blink = NET_LED_GREEN
    _thread.start_new_thread(blink_net_led_green, ())

def stop_blink_NET_LED():
    global net_led_blink
    net_led_blink = None
    




