from machine import UART, Pin
import time
import TinyFrame as TF
from do_update import *
from cmd_id import *
import beep
import lock
import LED

    
def fallback_listener(tf, frame):
    #print(frame)
    if frame.type == OBJID_KEY:
        update_key(frame)
    elif frame.type == OBJID_SWITCH:
        update_switch(frame)
    elif frame.type == OBJID_BAT:
        update_battery(frame)
    elif frame.type == OBJID_TEMP:
        update_temperature(frame)
    

p3v3 = Pin(46, Pin.OUT)
p3v3.on()

p5v = Pin(45, Pin.OUT)
p5v.on()

uart1 = UART(1, baudrate=115200, tx=5, rx=4)
tf = TF.TinyFrame(0)
tf.CKSUM_TYPE = 'crc16'
tf.ID_BYTES = 1
tf.LEN_BYTES = 2
tf.TYPE_BYTES = 2
tf.write = uart1.write
# Add listeners
tf.add_fallback_listener(fallback_listener)

beep.init(tf)
lock.init(tf)
#LED.init()
#tf.send(0x19,bytearray([0,2,0,0]))
while True:
    c = uart1.read(1)
    if c is not None:
        tf.accept(c)
    time.sleep_ms(1)

