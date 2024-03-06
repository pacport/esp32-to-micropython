from pmqtt import AWSMqtt
from authMqtt import get_client, thingName
from AWSConfig import *

import time
import ujson
import ubinascii

mqtt_client = get_client()
jobId=None
streamId=None
fileName=None
fileSize = None

stream = None
download_status = None
mesg = ujson.dumps({
    "state": {
    },
    'c': '123456',
})
def subscribe_callback(topic, msg):
    global jobId, streamId, fileName, fileSize, download_status
    topic = str(topic, 'utf-8')
    message = ujson.loads(msg)
    if topic == '$aws/things/PabbitLite_PP1AVBBJ3000450/jobs/get/accepted':
        jobId = message['inProgressJobs'][0]['jobId']
    if topic == '$aws/things/PabbitLite_PP1AVBBJ3000450/jobs/start-next/accepted':
        global streamId, fileName, fileSize
        streamId = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['streamId']
        fileName = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['fileName']
        fileSize = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['fileSize']
        
        mqtt_client.publish(AWS_TOPIC_STREAMS_DESCRIBE.format(mqtt_client.thingName, streamId), mesg)
    elif topic == AWS_TOPIC_STREAMS_DESCRIPTION.format(mqtt_client.thingName, streamId):
        global stream
        stream = message
    elif topic == AWS_TOPIC_STREAM_DATA.format(mqtt_client.thingName, streamId):
        sequence_number = message['i']
        if download_status is None:
            print('download_status error! value: None')
            return
        if sequence_number != download_status:
            print('sequence_number error!')
            return
        print(sequence_number)
        download_status = None
        if sequence_number == 0:
            try:
                import os
                os.remove("example.apk")
                print("文件删除成功")
            except OSError as e:
                print(f"删除失败: {e}")
        data = message['p']
        decoded_data = ubinascii.a2b_base64(data)
        with open("example.apk", "ab") as file:
            # 写入要追加的字节数据
            file.write(decoded_data)



mqtt_client.set_callback(subscribe_callback)



mqtt_client.publish(AWS_TOPIC_JOBS_START_NEXT.format(mqtt_client.thingName), mesg)
    
MAX_DATA_SIZE = 1024*50
while stream is None:
    time.sleep(1)
print(stream)
fileSize = stream['r'][0]['z']

start_time = time.time()
fullBlockNumber = int(fileSize / MAX_DATA_SIZE)
lastBlockFileSize = fileSize % MAX_DATA_SIZE

for i in range(fullBlockNumber):
    mesg = ujson.dumps({
            'c': stream['c'],
            's': stream['s'],
            'f': stream['r'][0]['f'],
            'l': MAX_DATA_SIZE,
            'o': i,
            'n':1,

    })
    download_status = i
    mqtt_client.publish(AWS_TOPIC_STREAM_GET.format(mqtt_client.thingName, streamId), mesg)
    while download_status == i:
        for _ in range(100):
            time.sleep_ms(10)
            if download_status is None:
                break
        if download_status == i:
            mqtt_client.publish(AWS_TOPIC_STREAM_GET.format(mqtt_client.thingName, streamId), mesg)
            print('republished')
            
mesg = ujson.dumps({
        'c': stream['c'],
        's': stream['s'],
        'f': stream['r'][0]['f'],
        'l': lastBlockFileSize,
        'o': fullBlockNumber,
        'n':1,

})
print(fullBlockNumber)
download_status = fullBlockNumber
mqtt_client.publish(AWS_TOPIC_STREAM_GET.format(mqtt_client.thingName, streamId), mesg)
while download_status == fullBlockNumber:
    for _ in range(10):
        time.sleep_ms(100)
        if download_status is None:
            break
    if download_status == fullBlockNumber:
        mqtt_client.publish(AWS_TOPIC_STREAM_GET.format(mqtt_client.thingName, streamId), mesg)
        print('republished')
execution_time = time.time() - start_time
print("下载耗时：", execution_time, "秒")
while True:
    time.sleep(1)

