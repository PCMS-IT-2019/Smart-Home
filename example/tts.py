import sys
from speech.stream import *
from speech.api import *
from playsound import playsound

'''语音合成范例'''

def main():
    # 一定要保存为.mp3格式
    filename = '../speech/audio/tts.mp3'
    save_recordFrames(filename,synthesis('百度语音'))
    playsound(filename)

if __name__ == '__main__':
    sys.exit(main())