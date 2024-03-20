import network
from machine import Pin,SPI
import utime
import ujson
import esp_audio
import ubinascii
import TCA9555

MAC = network.WLAN().config('mac')
MAC = ubinascii.hexlify(MAC).decode()
print("MAC:",MAC)

Networking = None
def test_network():
    try:
        import urequests
        res = urequests.get("https://iot.pacport.com")
        res.close()
        return True
    except:
        return False
def connectEthernet():
    Pin(46, Pin.OUT).on();Pin(45, Pin.OUT).on()
    utime.sleep_ms(100)
    hspi = SPI(1, 10000000, sck=Pin(1), mosi=Pin(2), miso=Pin(10))
    l = network.LAN(phy_addr=1, phy_type=network.PHY_DM9051,spi=hspi,mdc=Pin(16), mdio=Pin(17))
    try:
        l.active(True)
    except:
        pass
    for i in range(300):
        utime.sleep_ms(10)
        if l.ifconfig()[0] != '0.0.0.0':
            print(l.ifconfig())
            return True
    return False
    
def connectWIFI(wifiCfg=None):
    try:
        if wifiCfg is None:
            with open('wifipassword.json', 'r') as f:
                wifiCfg= ujson.loads(f.read())
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if wlan.isconnected():
            pass
            #wlan.disconnect()
        print(wifiCfg)
        if len(wifiCfg['ssid']) > 0 and len(wifiCfg['pwd']) > 3:
            if not wlan.isconnected():
                wlan.connect(wifiCfg['ssid'], wifiCfg['pwd'])
                
            for i in range(50):
                utime.sleep_ms(100)
                if wlan.isconnected():
                    break
        if wlan.isconnected():
            esp_audio.play("embed://tone/15_wifi_config_success.mp3")
            f = open('wifipassword.json', 'w')
            f.write(ujson.dumps(wifiCfg))
            f.close()
            return
        wlan.disconnect()
    except:
        pass
    esp_audio.play("embed://tone/16_wifi_conn_failed.mp3")      

def connect(wifiCfg=None):
    global Networking
    if Networking is not None:
        return Networking
    TCA9555.blink_NET_LED_GREEN()
    if wifiCfg is not None or connectEthernet() == False:
        print("use wifi")
        TCA9555.blink_NET_LED_RED()
        connectWIFI(wifiCfg)
        Networking = 'Wifi'
    else:
        Networking = 'Ethernet'
        
    TCA9555.stop_blink_NET_LED()
    if test_network():
        TCA9555.tca9555.set_gpio(TCA9555.NET_LED_RED, 1)
        TCA9555.tca9555.set_gpio(TCA9555.NET_LED_GREEN, 0)
    else:
        TCA9555.tca9555.set_gpio(TCA9555.NET_LED_RED, 0)
        TCA9555.tca9555.set_gpio(TCA9555.NET_LED_GREEN, 1)
        Networking = None
    return Networking  
