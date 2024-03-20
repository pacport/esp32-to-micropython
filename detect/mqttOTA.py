from mqtt import AWSMqtt
from mqttAuth import get_client
from AWSConfig import *

import time
import ujson
import ubinascii
from esp32 import Partition
import machine
VERSION = '2.0.2'
mqtt_client = get_client()
jobId=None
streamId=None
fileName=None
fileSize = None
fileName = None
stream = None
download_status = None
software_version = None
mesg = ujson.dumps({
    "state": {
    },
    'c': '123456',
})
def subscribe_callback(topic, msg):
    global jobId, streamId, fileName, fileSize, download_status, software_version
    topic = str(topic, 'utf-8')

    message = ujson.loads(msg)
    #if topic == '$aws/things/PabbitLite_PP1AVBBJ3000450/jobs/get/accepted':
        #print(message)
        #jobId = message['inProgressJobs'][0]['jobId']
    if topic == AWS_TOPIC_JOBS_START_NEXT_ACCEPTED.format(mqtt_client.thingName):
        try:
            if message['execution']['jobDocument'][0]['steps'][0]['action']['type'] == 'OTAUpdate':
                software_version = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['software-version']
                if software_version > VERSION:
                    streamId = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['streamId']
                    fileName = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['fileName']
                    fileSize = message['execution']['jobDocument'][0]['steps'][0]['action']['info']['fileSize']
                    print("OTA is larger version, Will do upgrade")
                else:
                    print("OTA is smaller version, Will not upgrade")
        except:
            print("no jobs")
        

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
                os.remove(fileName)
                print("文件删除成功")
            except OSError as e:
                print(f"删除失败: {e}")
        data = message['p']
        decoded_data = ubinascii.a2b_base64(data)
        with open(fileName, "ab") as file:
            # 写入要追加的字节数据
            file.write(decoded_data)





def check_upgrade_task():
    mqtt_client.set_callback(subscribe_callback)
    #mqtt_client.subscribe('$aws/things/PabbitLite_PP1AVBBJ3000450/jobs/start-next/accepted')
    print("start: check_upgrade_task")
    mqtt_client.publish(AWS_TOPIC_JOBS_START_NEXT.format(mqtt_client.thingName), mesg)
    for _ in range(200):
        mqtt_client.check_msg()
        if fileSize is not None:
            return True
        time.sleep_ms(10)
    return False
def download_OTA_file():
    print("start: download_OTA_file")
    mqtt_client.publish(AWS_TOPIC_STREAMS_DESCRIBE.format(mqtt_client.thingName, streamId), ujson.dumps({"state": {},'c': '123456',}))
    for _ in range(200):
        mqtt_client.check_msg()
        if stream is not None:
            break
        time.sleep_ms(10)
    if stream is None:
        return False
    MAX_DATA_SIZE = 1024*50
    fileSize = stream['r'][0]['z']
    fullBlockNumber = int(fileSize / MAX_DATA_SIZE)
    lastBlockFileSize = fileSize % MAX_DATA_SIZE
    global download_status
    for i in range(fullBlockNumber + 1):
        data_size = MAX_DATA_SIZE
        if i == fullBlockNumber:
            data_size = lastBlockFileSize
        mesg = ujson.dumps({
                'c': stream['c'],'s': stream['s'],
                'f': stream['r'][0]['f'],
                'l': data_size, 'o': i, 'n':1,})
        download_status = i
        mqtt_client.publish(AWS_TOPIC_STREAM_GET.format(mqtt_client.thingName, streamId), mesg)
        while download_status == i:
            for _ in range(100):
                mqtt_client.check_msg()
                time.sleep_ms(10)
                if download_status is None:
                    break
            if download_status == i:
                mqtt_client.publish(AWS_TOPIC_STREAM_GET.format(mqtt_client.thingName, streamId), mesg)
                print('OTA republished')
    return True
def write_OTA_file_to_flash():
    SEC_SIZE = 4096
    buf = bytearray(SEC_SIZE)
    i = 0
    currentPartition = Partition(Partition.RUNNING)
    nextPartition = currentPartition.get_next_update()
    assert nextPartition.ioctl(5,0) == SEC_SIZE
    SEC_COUNT = nextPartition.ioctl(4,0)
    with open(fileName, 'r') as f:
        buf = f.read(SEC_SIZE)
        if int(i/SEC_SIZE) > SEC_COUNT:
            print("attempt to write more sectors than available")
        if buf:
            if len(buf) < SEC_SIZE:
                print('adding padding to sector')
                buf = buf + bytes(b'\xff'*(4096 - len(buf)))
                nextPartition.writeblocks(int(i/SEC_SIZE), buf)
                nextPartition.set_boot()
                currentPartition.mark_app_valid_cancel_rollback()
                machine.reset()
            nextPartition.writeblocks(int(i/SEC_SIZE), buf)
            i += SEC_SIZE
def check_download_write_reboot():      
    if check_upgrade_task():
        print("OTA start download")
        start_time = time.time()
        if download_OTA_file():
            print("OTA download OK")
            execution_time = time.time() - start_time
            print("下载耗时：", execution_time, "秒")
            write_OTA_file_to_flash()
    else:
        print("do not need OTA upgrade")
 

