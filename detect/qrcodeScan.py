from machine import UART
import LED
import time

cmdlist = [
	"SCAN",          #扫码
	"MANTRI0",       #脉冲触发
	"MDTDTO",        #扫描超时
	"232UTF1",       #输出UTF8
	"LAMBRI",        #补光灯亮??
	"SCMMDT",        #移动侦测开
	"MDTHR",         #移动侦测灵敏??
	"MIDMIT",        #移动侦测休眠
	"I25CHK0",       #无校验位
    "PACKEN0",       #无包头包尾
	"CDBMIN4",       #最小长度设??
	"CAPTRUE JPEG-", #拍照
    "GET JPGINFO",   #获取照片信息
    "GET JPEG",      #获取照片文件
    "SLEEP",
    "DSPYFW",        #获取版本??
    "POR232",        #UART MODE
    "232BAD9",       #115200
    "232BAD10",      #230400
    "232BAD12",      #921600
    "SETSAV",
    "ODCENA",  #允许所有一维码
    "QRCENA1",  #允许所有二维码
]
uart1 = UART(2, baudrate=115200, tx=7, rx=15)
LED.init()
LED.set_GPIO(LED.QR_TRIG, 1)
uart1.write('^_^QRCENA.')
time.sleep_ms(20)
uart1.write('^_^QRCENA1.')
time.sleep_ms(20)
uart1.flush()
uart1.write('^_^SCAN.')

while True:
    c = uart1.readline()
    if c is not None and len(c) > 5:
        print(c[:-1])
    time.sleep_ms(1)