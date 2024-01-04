# 编译esp32s3 camera固件
## 1. env :
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html

## 2. 
```shell
mkdir ~/esp
cd ~/esp
git clone -b v5.0.2 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh 
. ./export.sh


cd ..
git clone https://github.com/espressif/esp32-camera.git
mv esp32-camera esp-idf/components

git clone -b v1.21.0 https://github.com/micropython/micropython.git

git clone https://github.com/lemariva/micropython-camera-driver.git

cp -rf micropython-camera-driver/src micropython/ports/esp32

cd micropython/ports/esp32

echo 'CONFIG_GC2145_SUPPORT=y' >> boards/ESP32_GENERIC_S3/sdkconfig.board
echo '#define MODULE_CAMERA_ENABLED  (1)' >> boards/ESP32_GENERIC_S3/mpconfigboard.h

make BOARD=ESP32_GENERIC_S3 submodules
make USER_C_MODULES=../src/micropython.cmake BOARD=ESP32_GENERIC_S3 all
```
```python
from machine import Pin, I2C
import camera
import time


PORT0_INPUT = 0x00
PORT1_INPUT = 0x01
PORT0_OUTPUT = 0x02
PORT1_OUTPUT = 0x03
PORT0_COMFIG = 0x06
PORT1_COMFIG = 0x07
OUTPUT_MODE = b'\x00'
INPUT_MODE = b'\xff'

CAM_EN = 0x40
i2c_addr = 32


p3v3 = Pin(46, Pin.OUT)
p3v3.on()
p5v = Pin(45, Pin.OUT)
p5v.on()

def to_byte(integer: int, n=1):
    return integer.to_bytes(n, "big")
i2c = I2C(scl=Pin(18),sda=Pin(17),freq=100000)
i2c.writeto_mem(i2c_addr, PORT0_COMFIG, OUTPUT_MODE)
i2c.writeto_mem(i2c_addr, PORT1_COMFIG, OUTPUT_MODE)

i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, to_byte(0xff)) # Initial value is 0xff
i2c.writeto_mem(i2c_addr, PORT1_OUTPUT, to_byte(0x79)) # Initial value is 0x79

def read_PORT0():
    return int.from_bytes(i2c.readfrom_mem(i2c_addr, PORT0_INPUT, 1), "big")
def set_GPIO(pins, status):
    if pins < 256:
        data = read_PORT0()
        if status == 1:
            data = data | pins
        else:
            data = data & ~pins
        i2c.writeto_mem(i2c_addr, PORT0_OUTPUT, to_byte(data))

set_GPIO(CAM_EN, 0)
time.sleep_ms(10)
set_GPIO(CAM_EN, 1)
time.sleep_ms(10)

camera.init(0, d0=13, d1=47, d2=14, d3=3, d4=12, d5=42, d6=41, d7=39,
            format=camera.RGB565, framesize=camera.FRAME_SVGA, 
            xclk_freq=camera.XCLK_20MHz,
            href=38, vsync=21, reset=-1, pwdn=-1,
            sioc=18, siod=17, xclk=40, pclk=11, fb_location=camera.PSRAM)

buf = camera.capture()

```

camera.init() 函数中的参数是参考PP1A-Pro/main/qcam_driver.c 中以下的摄像头初始化参数 :

```c

#define CAM_PIN_PWDN    -1  //power down is not used
#define CAM_PIN_RESET   -1 //software reset will be performed
#define CAM_PIN_XCLK    40
#define CAM_PIN_SIOD    17
#define CAM_PIN_SIOC    18

#define CAM_PIN_D7      39
#define CAM_PIN_D6      41
#define CAM_PIN_D5      42
#define CAM_PIN_D4      12
#define CAM_PIN_D3      3
#define CAM_PIN_D2      14
#define CAM_PIN_D1      47
#define CAM_PIN_D0      13
#define CAM_PIN_VSYNC   21
#define CAM_PIN_HREF    38
#define CAM_PIN_PCLK    11

#define CAM_MAX_RETRY_TIMES 3

.xclk_freq_hz = 20000000, //20000000,
.ledc_timer = LEDC_TIMER_0,
.ledc_channel = LEDC_CHANNEL_0,

.pixel_format = PIXFORMAT_RGB565, //YUV422,GRAYSCALE,RGB565,JPEG
.frame_size = FRAMESIZE_SVGA, //FRAMESIZE_SVGA, //FRAMESIZE_XGA, //FRAMESIZE_QVGA, //QQVGA-UXGA Do not use sizes above QVGA when not JPEG

.jpeg_quality = 54, //0-63 lower number means higher quality
.fb_count = 1, //1       //if more than one, i2s runs in continuous mode. Use only with JPEG
.fb_location = CAMERA_FB_IN_PSRAM,
.grab_mode = CAMERA_GRAB_WHEN_EMPTY, //CAMERA_GRAB_LATEST
.sccb_i2c_cbr = NULL,
```