import urequests
import ujson
from connectNetwork import MAC
from machine import RTC
from md5 import cparser_md5, flashid_hash


devid = '58013C41AC6375A9'
SN = 'PP1AVBBJ3000450'
APP_DEV_SEC = "Q3R0XWZpv4mKuYEBtgCzIiGlNokDbMUSVnP7aHL9hcdq5JFAx6fsOy2w18rjeT"
APP_DEV_KEY = "PP1A"
def regist(sn=SN):
    try:
        ip = "https://iot.pacport.com/v1/device/"
        now_url = ip + dev_id +'/now.do'
        res = urequests.get(now_url, headers = {'content-type': 'application/json'}).json()
        timestamp = res['data']['timestamp']
        
        tonke_url = ip + dev_id + "/token.do?timestamp=" + str(timestamp)
        auth = str(timestamp) + APP_DEV_SEC
        auth = cparser_md5(auth)
        auth = APP_DEV_KEY + ':' + auth
        res = urequests.get(tonke_url, headers = {'content-type': 'application/json', 'Authorization':auth}).json()
        token = res['data']['token']
        
        print(token)
        flashid = flashid_hash('PP1A' + ':'+'FFFE' + MAC)
        print('PP1A' + ':'+'FFFE' + MAC)
        print(flashid)
        post_data = ujson.dumps({ 'baseMac': 'FFFE'+MAC, 'flashId': flashid, 'sn': sn})
        request_url = ip + dev_id +'/burn/data.do'
        res = urequests.post(request_url,
                            headers = {'content-type': 'application/json', 'X-REQUEST-TOKEN':token},
                            data=post_data).json()
        info = ujson.dumps(res['data'])
        def xhash_bkdr2(str):
            len = len(str)
            hash = 0
            seed = 131
            for i in range(len):
                hash = (hash * seed) + ord(str[i])

            return hash & 0x7FFFFFFF
        magic_str = "%08X" % xhash_bkdr2(sn)
        post_data = ujson.dumps({ 'magic':magic_str,'flashId': flashid, 'sn': sn, 'verifyResult':0})
        request_url = ip + dev_id +'/burn/confirm.do'
        res = urequests.post(request_url,
                            headers = {'content-type': 'application/json', 'X-REQUEST-TOKEN':token},
                            data=post_data).json()
        print(res)
    except:
        print("sn regist error")
