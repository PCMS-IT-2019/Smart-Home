import sys
from recorder import *
from aip import AipSpeech

def main():
    sensitivity = input_loop("請輸入靈敏度(0至1之間，越大越靈敏，初始測試建議設定0.7)：")
    if(not iscalibrated()):input("請確保周圍安靜並且你在按下Enter後5秒內說出“百度語音”")
    min_amplitude = calibrate(sensitivity)
    print("閾值為："+str(min_amplitude))
    pcm = get_talkOnce()
    save_recordFrames("test.pcm",pcm)
    '''在此处添加语音识别'''
    # create接口
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    response = client.asr(pcm, 'pcm', 16000, {
        'dev_pid': 1536,
    })
    print(response)

if __name__ == '__main__':
    sys.exit(main())