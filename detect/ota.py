import network
from time import sleep
import audio
print(audio.verno())
sta_if = network.WLAN(network.STA_IF)

ssid = " "
password = " "
if not sta_if.isconnected():
    sta_if.active(True)
    print('connecting to network...')
    # TODO remove hard coded BSSID and figure out how to connect to the "strongest" signal
    sta_if.connect(ssid,password)
    while not sta_if.isconnected():
        print('.', end = '')
        sleep(0.25)
try:
    host = sta_if.config('hostname')
except ValueError:
    # "hostname" is available in master, but not yet in June 2022 1.19.1 release
    host = sta_if.config('dhcp_hostname')
print('Wifi connected as {}/{}, net={}, gw={}, dns={}'.format(host, *sta_if.ifconfig()))

import urequests
res = urequests.get('http://10.0.1.13/micropython.bin')
print(type(res))


from esp32 import Partition
import machine

SEC_SIZE = 4096
buf = bytearray(SEC_SIZE)
i = 0
currentPartition = Partition(Partition.RUNNING)
nextPartition = currentPartition.get_next_update()
assert nextPartition.ioctl(5,0) == SEC_SIZE
SEC_COUNT = nextPartition.ioctl(4,0)
while True:
    if int(i/SEC_SIZE) > SEC_COUNT:
        print("attempt to write more sectors than available")
    buf = res.content[i:i+SEC_SIZE]
    if buf:
        print("i:",i)
        print("len(buf):",len(buf))
        print("i/SEC_SIZE:", i/SEC_SIZE)
        if len(buf) < SEC_SIZE:
            print('adding padding to sector')
            buf = buf + bytes(b'\xff'*(4096 - len(buf)))
            nextPartition.writeblocks(int(i/SEC_SIZE), buf)
            nextPartition.set_boot()
            machine.reset()
        nextPartition.writeblocks(int(i/SEC_SIZE), buf)
        i += SEC_SIZE
    else:
        break

