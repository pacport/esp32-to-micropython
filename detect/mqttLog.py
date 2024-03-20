from mqttAuth import get_client
import ujson
from AWSConfig import *

class Log:
    def __init__(self):
        self.mqtt_client = get_client()
        self.thingName = self.mqtt_client.thingName
    

    def make_msg(self, msg):
        return ujson.dumps({
            "timestamp": 1234567,
            "msg": msg
        })

    def send(self, msg):
        self.mqtt_client.publish(AWS_TOPIC_LOG.format(self.thingName), self.make_msg(msg))
    def send_error(self, msg):
        self.mqtt_client.publish(AWS_TOPIC_ERROR_LOG.format(self.thingName), self.make_msg(msg))