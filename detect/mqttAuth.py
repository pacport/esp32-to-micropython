import mqtt
from mqtt import AWSMqtt
import AWSConfig
import os
import time
import ujson
#from AWSConfig import *


mqtt_client = None

certificatePem = None
certificateId = None
certificateOwnershipToken = None
privateKey = None
thingName = None
mqtt = None
stream = None
topic_pub = '$aws/certificates/create/json'
topic_step1_accepted = b'$aws/certificates/create/json/accepted'

topic_pub2 = '$aws/provisioning-templates/FleetTemplateForPabbitLiteV2/provision/json'
topic_step2_accepted = b'$aws/provisioning-templates/FleetTemplateForPabbitLiteV2/provision/json/accepted'
def subscribe_callback(topic, msg): 
    global certificatePem
    global certificateId
    global certificateOwnershipToken, thingName
    message = ujson.loads(msg)
    print(topic)
    if topic == topic_step1_accepted:
        try:
            certificatePem = message['certificatePem']
            certificateId = message['certificateId']
            certificateOwnershipToken = message['certificateOwnershipToken']
            privateKey = message['privateKey']
            
            f = open('cert.pem','w')
            f.write(certificatePem)
            f.close()
            
            f = open('private.key','w')
            f.write(privateKey)
            f.close()
            
            mesg = ujson.dumps({
                "certificateOwnershipToken": certificateOwnershipToken,
                "parameters": {
                "sn": "PP1AVBBJ3000450",
                "mac": "00016C06A629",
                "imei": "tiger-PP1AVBBJ3000450"
                }
            })
            mqtt_client.publish(topic_pub2, mesg)
        except Exception as e:
            print(e)
    if topic == topic_step2_accepted:
        thingName = message['thingName']
        
        

def connect():
    global mqtt_client, thingName
    import random
    client_id = str(random.randint(10000,100000))
    try:
        with open('private.key', 'r') as f:
            key = f.read()
        with open('cert.pem', 'r') as f:
            cert = f.read()
        with open('thingName.text', 'r') as f:
            thingName = f.read()
        ssl_params = {"key":key, "cert":cert, "server_side":False}
        print(thingName)
        mqtt_client = AWSMqtt(client_id, AWSConfig.endpoint, ssl_params, thingName)
        print("1 step auth OK")
        return mqtt_client
    except:
        print("CERTIFICATES CREATE")
        
    private_key = "private.pem.key"
    private_cert = "certificate.pem"
    with open(private_key, 'r') as f:
        key = f.read()
    with open(private_cert, 'r') as f:
        cert = f.read()
    ssl_params = {"key":key, "cert":cert, "server_side":False}
    mqtt_client = AWSMqtt(client_id, AWSConfig.endpoint, ssl_params)
    print("11111")
    mqtt_client.publish(topic_pub, '')
    mqtt_client.set_callback(subscribe_callback)
    
    
    while thingName is None:
        time.sleep_ms(100)
        mqtt_client.check_msg()
    print(thingName)
    f = open('thingName.text','w')
    f.write(thingName)
    f.close()
    
    
    with open('private.key', 'r') as f:
        key = f.read()
    with open('cert.pem', 'r') as f:
        cert = f.read()
    ssl_params = {"key":key, "cert":cert, "server_side":False}
    mqtt_client.reconnect(ssl_params)
    print("2 step auth OK")
    return mqtt_client
    
def get_client():
    global mqtt_client
    if mqtt_client is None:
       mqtt_client = connect()
    return mqtt_client


if __name__ == '__main__':
    get_client().set_callback(subscribe_callback)
    mesg = ujson.dumps({
        "state": {
            "desired": {
            },
            "reported": {
            }
        },
        #"clientToken": certificateOwnershipToken,
        "software-version": 'v0.0',
        "firmware-version": 'v0.0',
        'c': '123456',
    })
    AWS_TOPIC_JOBS = "$aws/things/"+ thingName +"/jobs"
    AWS_TOPIC_JOBS_GET = AWS_TOPIC_JOBS + "/get"
    print(AWS_TOPIC_JOBS_GET)
    get_client().publish(AWS_TOPIC_JOBS_GET, mesg)
    while True:
        mqtt_client.check_msg()
        time.sleep(1)
    
