from aip import AipNlp
from aip import AipSpeech

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

class baiduAip:
    def asr(self, audio):
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        response = client.asr(audio, 'pcm', 16000, {
            'dev_pid': DEV_PID.CN_ONLY.value,
        })
        return(response)

    def parser(self, text):
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        response = client.depParser(text)
        return(response)