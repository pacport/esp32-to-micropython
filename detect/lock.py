from machine import UART
import time
import TinyFrame as TF

class lock_action():
    IDLE = 0
    IN = 1
    OUT = 2
    STOP = 3
    SYNC =4

tf = None

def init(TinyFrame: TF):
    global tf
    tf = TinyFrame

def lock_move(atcion: lock_action):
     tf.send(0x41,bytearray([atcion,0,0,0]))

