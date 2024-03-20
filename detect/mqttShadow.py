from mqttAuth import get_client
import ujson
from AWSConfig import *
import time
from connectNetwork import Networking
from do_update import POWER_SOUCE, LEVEL
import do_update

mqtt_client = get_client() 
def subscribe_callback(topic, msg):
    pass

mqtt_client.set_callback(subscribe_callback)


mqtt_client.subscribe(SHADOW_TOPIC_GET_ACCEPTED.format(mqtt_client.thingName))
mqtt_client.subscribe(SHADOW_TOPIC_GET_REJECTED.format(mqtt_client.thingName))
mqtt_client.subscribe(SHADOW_TOPIC_UPDATE_ACCEPTED.format(mqtt_client.thingName))
mqtt_client.subscribe(SHADOW_TOPIC_UPDATE_REJECTED.format(mqtt_client.thingName))
print("mqtt Shadow sub OK")

def publish_shadow():
    mesg = ujson.dumps({
        "state": {
            "reported": {
                "network": Networking,
                "power_souce": POWER_SOUCE,
                'lock_state': do_update.Lock_state,
            }
        }
    })
    mqtt_client.publish(SHADOW_TOPIC_UPDATE.format(mqtt_client.thingName), mesg)
def get_shadow():
    mqtt_client.publish(SHADOW_TOPIC_GET.format(mqtt_client.thingName), '')
    
    
    
if __name__ == '__main__':
    publish_shadow()
    time.sleep(1)
    get_shadow()
    time.sleep(1)
