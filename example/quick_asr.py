import sys
from speech.rt_stream import *
from speech.api import *

'''极速短语音识别范例'''

def main():
    sensitivity = input_loop("請輸入靈敏度(0至1之間，越大越靈敏，初始測試建議設定0.7)：")
    if(not is_calibrated()):input("請確保周圍安靜並且你在按下Enter後5秒內說出“百度語音”")
    min_amplitude = calibrate(sensitivity)
    print("閾值為："+str(min_amplitude))
    while True:
        # 和之前的区别只是换了函数名称，quick_asr: 百度极速短语音识别api
        print(quick_asr(get_talkOnce(60)))

if __name__ == '__main__':
    sys.exit(main())