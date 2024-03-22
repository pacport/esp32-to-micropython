# esp32-to-micropython

# Flash bin to esp32
1. pip3 install esptool
2. esptool.py erase_flash
3. esptool.py -b 460800 --before default_reset --after no_reset --chip esp32s3  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m 0x0 bootloader/bootloader.bin 0x8000 partition_table/partition-table.bin 0x1c000 ota_data_initial.bin 0x20000 micropython.bin


