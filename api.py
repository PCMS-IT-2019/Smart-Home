from const import *
from aip import AipNlp
from aip import AipSpeech

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