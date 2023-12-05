### The example for Xmodem sender

#### Introduce

This example is a demo to introduce how to create a Xmodem sender and send data/file to Xmodem receiver.
The data or file will transmit over UART0 and  UART1 will output log.
For ESP8266, The data or file will transmit over UART0 and UART1 will output log.
For ESP32, The data or file will transmit over UART1, use IO17 as tx_pin, IO16 as rx_pin, IO15 as cts_pin and IO14 as rts_pin and UART0 will output log.

#### Prepare the build environment

Please refer the README file in root directory.

#### How to build

* enter the xmodem_sender example directory.
```
cd esp-xmodem/examples/xmodem_sender
```

* build the example
```
make defconfig
make flash
```
or use cmake
```
idf.py build
idf.py -p (PORT) flash monitor
```
#### Software prepare
In this example, user can use rz(More details please refer to root directory README file) to be as Xmodem receiver or use example xmodem_receiver to be as Xmodem receiver.

This example will first connect to WIFI, user can config WIFI ssid and password in
```
make menuconfig -> Example Connection Configuration
```

After config the WIFI ssid and password, user should config http server address, port and file name to download file from.
```
make menuconfig -> Example Configuration
```

Then user should deploy a http server for example downloading file. For python, it offers command `python -m SimpleHTTPServer` to start a http server. The http server root directory is in current command directory.
Last, user can surface `http://localhost:8000/` to test the web server can work right or not.

#### Example output
```
[17:40:44.678] ets Jan  8 2013,rst cause:1, boot mode:(3,7)
[17:40:44.678]
[17:40:44.678]load 0x40100000, len 7288, room 16 
[17:40:44.724]tail 8
[17:40:44.725]chksum 0x3b
[17:40:44.725]load 0x3ffe8408, len 24, room 0 
[17:40:44.725]tail 8
[17:40:44.725]chksum 0xb2
[17:40:44.725]load 0x3ffe8420, len 3336, room 0 
[17:40:44.725]tail 8
[17:40:44.783]chksum 0x28
[17:40:44.783]csum 0x28踇0;32mI (47) boot: ESP-IDF qa-test-v3.4-1112-16-g61c3c11-d 2nd stage bootloader[0m
[17:40:44.783][0;32mI (47) boot: compile time 10:04:26[0m
[17:40:44.783][0;32mI (51) qio_mode: Enabling default flash chip QIO[0m
[17:40:44.783][0;32mI (57) boot: SPI Speed      : 40MHz[0m
[17:40:44.783][0;32mI (64) boot: SPI Mode       : QIO[0m
[17:40:44.783][0;32mI (70) boot: SPI Flash Size : 2MB[0m
[17:40:44.783][0;32mI (76) boot: Partition Table:[0m
[17:40:44.783][0;32mI (81) boot: ## Label            Usage          Type ST Offset   Length[0m
[17:40:44.783][0;32mI (93) boot:  0 nvs              WiFi data        01 02 00009000 00006000[0m
[17:40:44.878][0;32mI (104) boot:  1 phy_init         RF data          01 01 0000f000 00001000[0m
[17:40:44.878][0;32mI (116) boot:  2 factory          factory app      00 00 00010000 000f0000[0m
[17:40:44.878][0;32mI (127) boot: End of partition table[0m
[17:40:44.878][0;32mI (134) esp_image: segment 0: paddr=0x00010010 vaddr=0x40210010 size=0x75b78 (482168) map[0m
[17:40:44.878][0;32mI (312) esp_image: segment 1: paddr=0x00085b90 vaddr=0x40285b88 size=0x160dc ( 90332) map[0m
[17:40:44.997][0;32mI (343) esp_image: segment 2: paddr=0x0009bc74 vaddr=0x3ffe8000 size=0x00680 (  1664) load[0m
[17:40:45.065][0;32mI (344) esp_image: segment 3: paddr=0x0009c2fc vaddr=0x40100000 size=0x00080 (   128) load[0m
[17:40:45.065][0;32mI (354) esp_image: segment 4: paddr=0x0009c384 vaddr=0x40100080 size=0x054a4 ( 21668) load[0m
[17:40:45.065][0;32mI (375) boot: Loaded app from partition at offset 0x10000[0m
[17:40:45.065][0;32mI (400) system_api: Base MAC address is not set, read default base MAC address from EFUSE[0m
[17:40:45.125][0;32mI (403) system_api: Base MAC address is not set, read default base MAC address from EFUSE[0m
[17:40:45.125]phy_version: 1163.0, 665d56c, Jun 24 2020, 10:00:08, RTOS new
[17:40:45.177][0;32mI (466) phy_init: phy ver: 1163_0[0m
[17:40:45.177][0;32mI (481) example_connect: Connecting to HUAWEI_888...[0m
[17:40:45.188][0;32mI (1768) wifi:state: 0 -> 2 (b0)
[17:40:46.472][0m[0;32mI (1782) wifi:state: 2 -> 3 (0)
[17:40:46.485][0m[0;32mI (1790) wifi:state: 3 -> 5 (10)
[17:40:46.493][0m[0;32mI (1829) wifi:connected with HUAWEI_888, aid = 1, channel 1, HT20, bssid = 34:29:12:43:c5:40
[17:40:46.549][0m[0;31mE (1839) wifi: AES PN: 0000000000000000 <= 0000000000000000[0m
[17:40:46.549][0;32mI (4270) tcpip_adapter: sta ip: 172.168.30.131, mask: 255.255.255.0, gw: 172.168.30.1[0m
[17:40:49.019][0;32mI (4275) example_connect: Connected to HUAWEI_888[0m
[17:40:49.019][0;32mI (4279) example_connect: IPv4 address: 172.168.30.131[0m
[17:40:49.019][0;32mI (4288) xmodem_send: Connected to AP, begin http client task[0m
[17:40:49.019][0;32mI (4298) uart: queue free spaces: 10[0m
[17:40:49.019][0;32mI (14300) xmodem_send: Connecting to Xmodem receiver(1/25)[0m
[17:40:59.011][0;32mI (23638) xmodem_send: ESP_XMODEM_EVENT_CONNECTED[0m
[17:41:08.349][0;32mI (24771) xmodem_send: Send image success[0m
```
