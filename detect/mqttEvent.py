from mqttAuth import get_client
from AWSConfig import *


mqtt_client = get_client() 
def subscribe_callback(topic, msg):
    pass

mqtt_client.set_callback(subscribe_callback)
mqtt_client.subscribe(TOPIC_Directive.format(mqtt_client.thingName))
print("mqtt Event sub OK")

