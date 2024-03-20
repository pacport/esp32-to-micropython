from machine import UART, Pin
import time
import TinyFrame as TF
from do_update import *
from cmd_id import *
import beep
import lock
import TCA9555
import _thread

    
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
    elif frame.type == OBJID_NFC_IN:
        nfc_in(frame)
    elif frame.type == OBJID_NFC_OUT:
        nfc_out(frame)
  

uart1 = UART(1, baudrate=115200, tx=5, rx=4)
tf = TF.TinyFrame(0)
tf.CKSUM_TYPE = 'crc16'
tf.ID_BYTES = 1
tf.LEN_BYTES = 2
tf.TYPE_BYTES = 2
tf.write = uart1.write
tf.add_fallback_listener(fallback_listener)

beep.init(tf)
lock.init(tf)
tf.send(0x19,bytearray([0,2,0,0]))
tf.send(0x46,bytearray([0,4,0x73,0,1,0])) # turn on nfc


import connectNetwork
def connect_net_and_mqtt():
    while connectNetwork.connect() is None:
        time.sleep(10)
        print("network connect retry")
    import mqttOTA
    mqttOTA.check_download_write_reboot()
    import mqttShadow
    import mqttEvent
    import mqttMsgHandle

_thread.start_new_thread(connect_net_and_mqtt, ())



while True:
    c = uart1.read(1)
    if c is not None:
        tf.accept(c)
    time.sleep_ms(1)

