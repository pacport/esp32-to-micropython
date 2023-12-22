from machine import UART, Pin
import time
import TinyFrame as TF

    
def fallback_listener(tf, frame):
    #print(frame.type)
    if frame.type == 0x10:
        if frame.data[2] == 0x02:
            print("button 1")
        elif frame.data[2] == 0x03:
            print("button 2")
        elif frame.data[2] == 0x04:
            print("button 3")
        elif frame.data[2] == 0x05:
            print("button 4")
        elif frame.data[2] == 0x06:
            print("button 5")
        elif frame.data[2] == 0x07:
            print("button 6")
        elif frame.data[2] == 0x08:
            print("button 7")
        elif frame.data[2] == 0x09:
            print("button 8")
        elif frame.data[2] == 0x0a:
            print("button 9")
        elif frame.data[2] == 0x01:
            print("button 0")
        elif frame.data[2] == 0x0b:
            print("button ESC")
        elif frame.data[2] == 0x0c:
            print("button OK")
    elif frame.type == 0x11:
        if frame.data[2] == 13:
            if frame.data[3] == 0x00:
                print("press power botton")
            elif frame.data[3] == 0x01:
                print("release power botton")
        elif frame.data[2] == 0x11:
            if frame.data[3] == 0x01 and frame.data[4] == 0x02:
                print("large lock is pressed in")
            elif frame.data[3] == 0x00 and frame.data[4] == 0x01:
                print("large lock is popped out")
        elif frame.data[2] == 0x0f:
            if frame.data[3] == 0x00 and frame.data[5] == 0x01:
                print("small lock is pressed in")
            elif frame.data[3] == 0x01 and frame.data[5] == 0x00:
                print("small lock is popped out")
    
p46 = Pin(46, Pin.OUT)
p46.on()

uart1 = UART(1, baudrate=115200, tx=5, rx=4)

tf = TF.TinyFrame(0)
tf.CKSUM_TYPE = 'crc16'
tf.ID_BYTES = 1
tf.LEN_BYTES = 2
tf.TYPE_BYTES = 2
tf.write = uart1.write

# Add listeners
tf.add_fallback_listener(fallback_listener)
while True:
    c = uart1.read(1)   # read a '\n' terminated line
    if c is not None:
        tf.accept(c)
    time.sleep_ms(10)

