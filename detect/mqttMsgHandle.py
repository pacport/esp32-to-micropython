import mqttEvent
import mqttShadow
from AWSConfig import *
from mqttAuth import get_client
import _thread
import time
from machine import Timer
import ujson
import lock

mqtt_client = get_client()
import hashlib
import random

def generate_uuid():
    # 使用当前时间戳和随机数生成唯一标识符
    timestamp = str(random.random()) + str(random.random()) + str(random.random())
    hashed_uuid = hashlib.sha1(timestamp.encode())
    # 将哈希对象的字节表示形式转换为十六进制字符串
    uuid_hex = ''.join(['{:02x}'.format(byte) for byte in hashed_uuid.digest()])
    return uuid_hex
def subscribe_callback(topic, msg):
    try:
        topic = str(topic, 'utf-8')
        message = ujson.loads(msg)
        if topic == TOPIC_Directive.format(mqtt_client.thingName):
            if message['directive']['header']['name'] == 'Unlock':
                lock.lock_move(lock.lock_action.IN)
                message['directive']['header']['name'] = "Unlocked"
            elif message['directive']['header']['name'] == 'Lock':
                lock.lock_move(lock.lock_action.OUT)
                message['directive']['header']['name'] = "Locked"
            message['directive']['header']['messageId'] = generate_uuid()
            mqtt_client.publish(TOPIC_Event.format(mqtt_client.thingName), ujson.dumps(message))
            print("pub :", message)
        elif topic == SHADOW_TOPIC_GET_ACCEPTED.format(mqtt_client.thingName):
            print("SHADOW_TOPIC_GET_ACCEPTED")
            print(message)
        elif topic == SHADOW_TOPIC_GET_REJECTED.format(mqtt_client.thingName):
            print("SHADOW_TOPIC_GET_REJECTED")
        elif topic == SHADOW_TOPIC_UPDATE_ACCEPTED.format(mqtt_client.thingName):
            print("SHADOW_TOPIC_UPDATE_ACCEPTED")
        elif topic == SHADOW_TOPIC_UPDATE_REJECTED.format(mqtt_client.thingName):
            print("SHADOW_TOPIC_UPDATE_REJECTED")
    except :
        print('subscribe_callback error')

mqtt_client.set_callback(subscribe_callback)
def report_shadow():
    mqttShadow.publish_shadow()
def check_mqtt_msg():
    i=0
    while True:
        
        mqtt_client.check_msg()
        time.sleep_ms(100)
        i += 1
        if i >= 100:
            i = 0
            report_shadow()
        
_thread.start_new_thread(check_mqtt_msg, ())



