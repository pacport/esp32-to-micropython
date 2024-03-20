import lock
import beep
import math
import TCA9555
from scanCode import sc

import esp_audio


def extract_data(frame):
    data = None
    if frame.data is not None and frame.len >= 6:
        data = frame.data[2:frame.len]
    return data

def update_key(frame):
        if frame.data[2] == 0x02:
            lock.lock_move(lock.lock_action.IN)
            print("button 1")
        elif frame.data[2] == 0x03:
            lock.lock_move(lock.lock_action.OUT)
            print("button 2")
        elif frame.data[2] == 0x04:
            beep.short()
            print("button 3")
        elif frame.data[2] == 0x05:
            beep.three_times_short()
            print("button 4")
        elif frame.data[2] == 0x06:
            beep.long()
            print("button 5")
        elif frame.data[2] == 0x07:
            if TCA9555.blinking_bat == False:
                TCA9555.start_blink_led(TCA9555.leds.BAT_LED_GREEN)
            else:
                TCA9555.stop_blink_led(TCA9555.leds.BAT_LED_GREEN)
            print("button 6")
        elif frame.data[2] == 0x08:
            if TCA9555.blinking_net == False:
                TCA9555.start_blink_led(TCA9555.leds.NET_LED_GREEN)
            else:
                TCA9555.stop_blink_led(TCA9555.leds.NET_LED_GREEN)
            print("button 7")
        elif frame.data[2] == 0x09:
            if TCA9555.blinking_net == False:
                TCA9555.start_blink_led(TCA9555.leds.NET_LED_RED)
            else:
                TCA9555.stop_blink_led(TCA9555.leds.NET_LED_RED)
        elif frame.data[2] == 0x0a:
            print("button 9")
        elif frame.data[2] == 0x01:
            print("button 0")
        elif frame.data[2] == 0x0b:
            print("button ESC")
        elif frame.data[2] == 0x0c:
            print("button OK")
            esp_audio.play("embed://tone/15_wifi_config_success.mp3")
    
Lock_state = "--"
def update_switch(frame):
    if frame.data[2] == 13:
        if frame.data[3] == 0x00:
            print("press power botton")
            sc.get_BARorQRcode()
        elif frame.data[3] == 0x01:
            print("release power botton")
    elif frame.data[2] == 0x11:
        if frame.data[3] == 0x01 and frame.data[4] == 0x02:
            global Lock_state
            Lock_state = "IN"
            print("large lock is pressed in")
        elif frame.data[3] == 0x00 and frame.data[4] == 0x01:
            global Lock_state
            Lock_state = "OUT"
            print("large lock is popped out")
    elif frame.data[2] == 0x0f:
        if frame.data[3] == 0x00 and frame.data[5] == 0x01:
            print("small lock is pressed in")
        elif frame.data[3] == 0x01 and frame.data[5] == 0x00:
            print("small lock is popped out")
            

_NTC_R_SERIES    =    10000.0
_NTC_R_NOMINAL   =    10000.0
_NTC_TEMP_NOMINAL =   25.0
_NTC_ADC_MAX      =   4095 
_NTC_BETA         =   3950

#######################################################################################
def ntc_convertToC( adcValue):
    temp = 0
    rntc = _NTC_R_SERIES / ((_NTC_ADC_MAX / adcValue ) - 1.0)
    temp = rntc / _NTC_R_NOMINAL
    temp = math.log(temp)
    temp /= _NTC_BETA
    temp += 1.0 / (_NTC_TEMP_NOMINAL + 273.15)
    temp = 1.0 / temp
    temp -= 273.15
    return temp



def update_temperature(frame):
    data = extract_data(frame)
    if data is not None:
        temp_adc = data[0]
        temp_ceil = data[1]
        #volt = ntc_convertToC(temp_adc)
        #print(f"ADC: {volt}, temp_ceil: {temp_ceil}℃")

POWER_SOUCE = None
LEVEL = None
def update_battery(frame):
    global POWER_SOUCE, LEVEL
    data = extract_data(frame)
    power_reason = data[0] + data[1]*256
    volt = data[2] + data[3]*256
    level= data[4] + data[5]*256
    mode = data[6] + data[7]*256
    if mode == 1:
        POWER_SOUCE = "BAT"
    elif mode == 2:
        POWER_SOUCE = "USB"
    elif mode == 4:
        POWER_SOUCE = "POE"
    LEVEL = level
    print(f"PWR: {power_reason}, VOLT: {volt}, LEVEL:{level}, MODE:{mode}")
    
    

def nfc_in(frame):
    print("nfc card was touched")
    data = extract_data(frame)
    uid_len = data[1]
    meta_len = data[2]
    print("uid= " + data[3:uid_len])
    print("meta= " + data[3+uid_len:meta_len])

def nfc_out(frame):
    print("nfc card was removed")