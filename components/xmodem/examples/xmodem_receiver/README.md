### The example for Xmodem receiver

#### Introduce

This example is a demo to introduce how to create a Xmodem receiver and receive data/file to OTA from Xmodem sender.
For ESP8266, The data or file will transmit over UART0 and UART1 will output log.
For ESP32, The data or file will transmit over UART1, use IO17 as tx_pin, IO16 as rx_pin, IO15 as cts_pin and IO14 as rts_pin and UART0 will output log.

#### Prepare the build environment

Please refer the README file in root directory.

#### How to build

* enter the xmodem_receiver example directory.
```
cd esp-xmodem/examples/xmodem_receiver
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
In this example, user can use sz(More details please refer to root directory README file) to be as Xmodem sender or use example xmodem_sender to be as Xmodem sender.

#### Example output
```
[17:46:56.262] ets Jan  8 2013,rst cause:1, boot mode:(3,6)
[17:46:56.262]
[17:46:56.262]load 0x40100000, len 7288, room 16 
[17:46:56.271]tail 8
[17:46:56.293]chksum 0x3b
[17:46:56.293]load 0x3ffe8408, len 24, room 0 
[17:46:56.293]tail 8
[17:46:56.293]chksum 0xb2
[17:46:56.293]load 0x3ffe8420, len 3336, room 0 
[17:46:56.293]tail 8
[17:46:56.365]chksum 0x2b
[17:46:56.365]csum 0x2b踇0;32mI (45) boot: ESP-IDF qa-test-v3.4-1112-16-g61c3c11-d 2nd stage bootloader[0m
[17:46:56.365][0;32mI (46) boot: compile time 17:06:02[0m
[17:46:56.365][0;32mI (48) qio_mode: Enabling default flash chip QIO[0m
[17:46:56.365][0;32mI (55) boot: SPI Speed      : 40MHz[0m
[17:46:56.365][0;32mI (62) boot: SPI Mode       : QIO[0m
[17:46:56.365][0;32mI (68) boot: SPI Flash Size : 2MB[0m
[17:46:56.365][0;32mI (74) boot: Partition Table:[0m
[17:46:56.365][0;32mI (80) boot: ## Label            Usage          Type ST Offset   Length[0m
[17:46:56.365][0;32mI (91) boot:  0 nvs              WiFi data        01 02 00009000 00004000[0m
[17:46:56.435][0;32mI (102) boot:  1 otadata          OTA data         01 00 0000d000 00002000[0m
[17:46:56.435][0;32mI (114) boot:  2 phy_init         RF data          01 01 0000f000 00001000[0m
[17:46:56.435][0;32mI (125) boot:  3 ota_0            OTA app          00 10 00010000 000f0000[0m
[17:46:56.435][0;32mI (137) boot:  4 ota_1            OTA app          00 11 00110000 000f0000[0m
[17:46:56.435][0;32mI (149) boot: End of partition table[0m
[17:46:56.435][0;32mI (155) boot: No factory image, trying OTA 0[0m
[17:46:56.448][0;32mI (163) esp_image: segment 0: paddr=0x00010010 vaddr=0x40210010 size=0x1e25c (123484) map[0m
[17:46:56.448][0;32mI (218) esp_image: segment 1: paddr=0x0002e274 vaddr=0x4022e26c size=0x07eac ( 32428) map[0m
[17:46:56.538][0;32mI (229) esp_image: segment 2: paddr=0x00036128 vaddr=0x3ffe8000 size=0x00554 (  1364) load[0m
[17:46:56.538][0;32mI (230) esp_image: segment 3: paddr=0x00036684 vaddr=0x40100000 size=0x00080 (   128) load[0m
[17:46:56.538][0;32mI (243) esp_image: segment 4: paddr=0x0003670c vaddr=0x40100080 size=0x04eb8 ( 20152) load[0m
[17:46:56.538][0;32mI (263) boot: Loaded app from partition at offset 0x10000[0m
[17:46:56.538][0;32mI (286) uart: queue free spaces: 10[0m
[17:46:56.575][0;32mI (3286) xmodem_receive: Waiting for Xmodem sender to send data...[0m
[17:46:59.580][0;32mI (6286) xmodem_receive: Waiting for Xmodem sender to send data...[0m
[17:47:02.618][0;32mI (6292) xmodem_receive: ESP_XMODEM_EVENT_CONNECTED[0m
[17:47:02.618][0;32mI (6294) xmodem_receive: This is a file begin transfer[0m
[17:47:02.618][0;32mI (6298) xmodem_receive: ESP_XMODEM_EVENT_ON_FILE[0m
[17:47:02.618][0;32mI (6306) xmodem_receive: file_name is xmodem_receiver.bin, file_length is 176704[0m
[17:47:02.618][0;32mI (6339) xmodem_receive: Starting OTA...[0m
[17:47:02.641][0;32mI (6340) xmodem_receive: Writing to partition subtype 17 at offset 0x110000[0m
[17:47:02.641][0;32mI (9305) xmodem_receive: esp_ota_begin succeeded[0m
[17:47:05.607][0;32mI (9306) xmodem_receive: Please Wait. This may take time[0m
[17:47:05.607][0;32mI (18056) xmodem_receive: Receive EOT data[0m
[17:47:14.388][0;32mI (18059) xmodem_receive: Receive EOT data again[0m
[17:47:14.388][0;32mI (18066) xmodem_receive: This is a file end transfer[0m
[17:47:14.388][0;32mI (18067) xmodem_receive: ESP_XMODEM_EVENT_FINISHED[0m
[17:47:14.388][0;32mI (18072) esp_image: segment 0: paddr=0x00110010 vaddr=0x40210010 size=0x1e248 (123464) map[0m
[17:47:14.388][0;32mI (18106) esp_image: segment 1: paddr=0x0012e260 vaddr=0x4022e258 size=0x07b10 ( 31504) map[0m
[17:47:14.461][0;32mI (18114) esp_image: segment 2: paddr=0x00135d78 vaddr=0x3ffe8000 size=0x00554 (  1364) [0m
[17:47:14.461][0;32mI (18119) esp_image: segment 3: paddr=0x001362d4 vaddr=0x40100000 size=0x00080 (   128) [0m
[17:47:14.461][0;32mI (18132) esp_image: segment 4: paddr=0x0013635c vaddr=0x40100080 size=0x04eb8 ( 20152) [0m
[17:47:14.461][0;32mI (18149) esp_image: segment 0: paddr=0x00110010 vaddr=0x40210010 size=0x1e248 (123464) map[0m
[17:47:14.461][0;32mI (18180) esp_image: segment 1: paddr=0x0012e260 vaddr=0x4022e258 size=0x07b10 ( 31504) map[0m
[17:47:14.531][0;32mI (18187) esp_image: segment 2: paddr=0x00135d78 vaddr=0x3ffe8000 size=0x00554 (  1364) [0m
[17:47:14.531][0;32mI (18192) esp_image: segment 3: paddr=0x001362d4 vaddr=0x40100000 size=0x00080 (   128) [0m
[17:47:14.531][0;32mI (18205) esp_image: segment 4: paddr=0x0013635c vaddr=0x40100080 size=0x04eb8 ( 20152) [0m
[17:47:14.531][0;32mI (18224) xmodem_receive: esp_ota_set_boot_partition succeeded[0m
[17:47:14.531]
[17:47:14.607] ets Jan  8 2013,rst cause:1, boot mode:(3,6)
[17:47:14.607]
[17:47:14.607]load 0x40100000, len 7288, room 16 
[17:47:14.607]tail 8
[17:47:14.628]chksum 0x3b
[17:47:14.628]load 0x3ffe8408, len 24, room 0 
[17:47:14.628]tail 8
[17:47:14.628]chksum 0xb2
[17:47:14.628]load 0x3ffe8420, len 3336, room 0 
[17:47:14.628]tail 8
[17:47:14.700]chksum 0x2b
[17:47:14.700]csum 0x2bm[0;32mI (85) boot: ESP-IDF qa-test-v3.4-1112-16-g61c3c11-d 2nd stage bootloader[0m
[17:47:14.700][0;32mI (85) boot: compile time 17:06:02[0m
[17:47:14.700][0;32mI (89) qio_mode: Enabling default flash chip QIO[0m
[17:47:14.700][0;32mI (104) boot: SPI Speed      : 40MHz[0m
[17:47:14.700][0;32mI (118) boot: SPI Mode       : QIO[0m
[17:47:14.700][0;32mI (130) boot: SPI Flash Size : 2MB[0m
[17:47:14.700][0;32mI (143) boot: Partition Table:[0m
[17:47:14.700][0;32mI (154) boot: ## Label            Usage          Type ST Offset   Length[0m
[17:47:14.700][0;32mI (177) boot:  0 nvs              WiFi data        01 02 00009000 00004000[0m
[17:47:14.768][0;32mI (200) boot:  1 otadata          OTA data         01 00 0000d000 00002000[0m
[17:47:14.768][0;32mI (223) boot:  2 phy_init         RF data          01 01 0000f000 00001000[0m
[17:47:14.768][0;32mI (246) boot:  3 ota_0            OTA app          00 10 00010000 000f0000[0m
[17:47:14.768][0;32mI (270) boot:  4 ota_1            OTA app          00 11 00110000 000f0000[0m
[17:47:14.768][0;32mI (293) boot: End of partition table[0m
[17:47:14.768][0;32mI (306) esp_image: segment 0: paddr=0x00110010 vaddr=0x40210010 size=0x1e248 (123464) map[0m
[17:47:14.781][0;32mI (392) esp_image: segment 1: paddr=0x0012e260 vaddr=0x4022e258 size=0x07b10 ( 31504) map[0m
[17:47:14.854][0;32mI (407) esp_image: segment 2: paddr=0x00135d78 vaddr=0x3ffe8000 size=0x00554 (  1364) load[0m
[17:47:14.854][0;32mI (414) esp_image: segment 3: paddr=0x001362d4 vaddr=0x40100000 size=0x00080 (   128) load[0m
[17:47:14.854][0;32mI (442) esp_image: segment 4: paddr=0x0013635c vaddr=0x40100080 size=0x04eb8 ( 20152) load[0m
[17:47:14.854][0;32mI (477) boot: Loaded app from partition at offset 0x110000[0m
[17:47:14.854][0;32mI (528) uart: queue free spaces: 10[0m
[17:47:14.886][0;32mI (3521) xmodem_receive: Waiting for Xmodem sender to send data...[0m
[17:47:17.883]
```
