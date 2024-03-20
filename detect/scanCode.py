from machine import UART
import TCA9555
import time
import _thread
import beep
import ujson
import connectNetwork

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
class ScanCode:
    def __init__(self):
        self.uart2 = UART(2, baudrate=115200, tx=7, rx=15)
        self.scaning = False
        self.uart2.write('^_^PACKEN0.')
        self.uart2.write('^_^CDBMIN5.')
        self.uart2.write('^_^QRCENA.')
        self.uart2.write('^_^QRCENA1.')
        self.uart2.write('^_^MDTDTO10.')
        self.uart2.write('^_^LAMBRI0.')
    def read_line(self, timeout):
        self.uart2.flush()
        timeout *= 100
        for _ in range(timeout):
            c = self.uart2.readline()
            if c is not None and len(c) > 5:
                self.scaning = False
                beep.short()
                self.code_handle(str(c, 'UTF-8'))
                return str(c, 'UTF-8')
            time.sleep_ms(10)
        print("no uart data")
        self.scaning = False
        beep.long()
        return None
    def get_BARorQRcode(self):
        if self.scaning == True:
            return
        def start_scan():
            self.scaning = True
            TCA9555.tca9555.set_gpio(TCA9555.QR_TRIG, 1)
            time.sleep_ms(1)
            TCA9555.tca9555.set_gpio(TCA9555.QR_TRIG, 0)
            #self.uart2.write('^_^SCAN.')
            self.uart2.flush()
            print("start scan")
            print(self.read_line(20))
        _thread.start_new_thread(start_scan, ())
        
    def code_handle(self, code_str):
        if code_str is None:
            return
        if code_str.find("WIFI:S:") == 0:
            code_str = code_str[5:]
            start = 0
            wifiCfg = {}
            for i, char in enumerate(code_str):
                if char == ';' and code_str[i-1] != '\\':
                    subStr = code_str[start:i]
                    if len(subStr) > 3 and subStr[0] == 'S':
                        wifiCfg['ssid'] = subStr[2:]
                    elif len(subStr) > 3 and subStr[0] == 'P':
                        wifiCfg['pwd'] = subStr[2:]
                    start = i + 1
            wifiCfg['ssid'] = wifiCfg['ssid'].replace("\\\\", "\\").replace("\\;", ";").replace("\\:", ":").replace("\\,", ",")
            wifiCfg['pwd'] = wifiCfg['pwd'].replace("\\\\", "\\").replace("\\;", ";").replace("\\:", ":").replace("\\,", ",")
            connectNetwork.connect(wifiCfg)
        elif code_str.find("PP1A") == 0:
            import regDevID
            print(code_str)
            regDevID.regist(code_str)
            
            
        


sc = ScanCode()