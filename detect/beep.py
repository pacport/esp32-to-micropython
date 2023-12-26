import TinyFrame as TF
import _thread
import time

QBEEP_HZ_KEY =      1980
QBEEP_HZ_SWITCH =   1980
QBEEP_HZ_NFC =      1980
QBEEP_HZ_ERROR =    1980
QBEEP_HZ_HIGH =     3520
QBEEP_HZ_LOW =      674

def init(TinyFrame: TF):
    global tf
    tf = TinyFrame
def do_beep(hz, ms, rep, gap):
    b_hz = hz.to_bytes(2, "little")
    b_ms = ms.to_bytes(2, "little")
    b_rep = rep.to_bytes(2, "little")
    b_gap = gap.to_bytes(2, "little")
    data = b_hz + b_ms + b_rep + b_gap
    tf.send(0x43, data)


def short():
    do_beep(QBEEP_HZ_KEY, 200, 0, 0)

def _do_three_times_short(arg1, arg2):
    do_beep(QBEEP_HZ_KEY, 200, 0, 0)
    time.sleep_ms(200)
    do_beep(QBEEP_HZ_KEY, 200, 0, 0)
    time.sleep_ms(200)
    do_beep(QBEEP_HZ_KEY, 200, 0, 0)
def three_times_short():
    _thread.start_new_thread(_do_three_times_short, (None, None))

def long():
    do_beep(QBEEP_HZ_KEY, 1000, 0, 0)
