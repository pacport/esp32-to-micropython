import network
import time
from audio import player
import TCA9555
from machine import Pin


def callback(stat):
    if stat['status'] != 1:
        TCA9555.tca9555.set_gpio(TCA9555.PA_CTRL, 1)




def play(sound):
    TCA9555.tca9555.set_gpio(TCA9555.PA_CTRL, 0)
    mPlayer.play(sound)
mPlayer = None
Pin(45, Pin.OUT).on()
TCA9555.tca9555.set_gpio(TCA9555.PA_CTRL, 0)
time.sleep_ms(20)
mPlayer=player(callback)
mPlayer.set_vol(70)

TCA9555.tca9555.set_gpio(TCA9555.PA_CTRL, 1)
print('Set volume to: ', mPlayer.get_vol())

