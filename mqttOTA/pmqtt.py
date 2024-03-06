import time
import network
from umqtt.simple import MQTTClient
from machine import Timer


class AWSMqtt:
    
    def __init__(self,clientID='port100', endpoint=None, sslp=None, thingName=None, subscribe_cb=None):
        self.clientID = clientID
        self.endpoint = endpoint
        self.thingName = thingName
        self.client = MQTTClient(client_id=clientID, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
        self.client.connect()
        self.recv_timer = Timer(0)
        if subscribe_cb is not None:
            self.client.set_callback(subscribe_cb)
            self.recv_timer.init(period=30, mode=Timer.PERIODIC, callback = lambda _:self.client.check_msg())
        
    
    def set_callback(self, subscribe_cb):
        self.client.set_callback(subscribe_cb)
        if self.recv_timer is not None:
            self.recv_timer.deinit()
        self.recv_timer = Timer(0)
        self.recv_timer.init(period=30, mode=Timer.PERIODIC, callback = lambda _:self.client.check_msg())
        
    def publish(self, topic, message):
        self.client.publish(topic, message)
        
    def subscribe(self, topic):
        self.client.subscribe(topic)
    
    
    def reconnect(self, sslp=None):
        self.disconnect()
        self.client = MQTTClient(client_id=self.clientID, server=self.endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
        self.client.connect()
    def disconnect(self):
        self.recv_timer.deinit()
        self.client.disconnect()
        
        
#Enter your wifi SSID and password below.
wifi_ssid = "AirPort1408"
wifi_password = "15202499574"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())
        
