from aip import AipNlp
from aip import AipSpeech
import requests
import json
import base64
import os
from speech.stream import *

from enum import Enum,unique
@unique
class DEV_PID(Enum):
    CN_MIX = 1536
    CN_ONLY = 1537
    EN = 1737
    CANTON = 1637

""" APPID AK SK """
APP_ID = '17956963'
API_KEY = 'y9umW9TaYizYaT6CyU08Bblv'
SECRET_KEY = 'NMGN6AnQoYE357VKY6Q6e9VzV0sdACtO'

TOKEN = "24.adcdcceea0c830b4ecff3c5d949ce009.2592000.1585219641.282335-17956963"

def asr(audio):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    response = client.asr(audio, 'pcm', 16000, {
        'dev_pid': DEV_PID.CN_ONLY.value,
    })
    return(response)

def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
    API_KEY, SECRET_KEY)
    response = requests.post(host)
    token = json.loads(response.text)["access_token"]
    print(token)
    return token

def quick_asr(audio):
    headers = {'Content-Type': 'application/json'}
    url = "https://vop.baidu.com/pro_api"
    data = {
        "format": "pcm",
        "cuid": "test1",
        "rate": RATE,
        "dev_pid": 80001,
        "speech": base64.b64encode(audio).decode('utf8'),
        "len": len(audio),
        "channel": 1,
        "token": TOKEN,
    }
    req = requests.post(url, json.dumps(data), headers)
    return json.loads(req.text)

def parser(text):
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    response = client.depParser(text)
    return(response)

def synthesis(text):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis('你好百度', 'zh', 1, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict
    if not isinstance(result, dict):
        return result
