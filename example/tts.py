import sys
from devices.speaker import *
from speech.api import *

'''语音合成范例'''

def main():
    speak(synthesis("今天天气不错，最高气温可达24度"))
    # speak(synthesis("已将空调调至24度"))

if __name__ == '__main__':
    sys.exit(main())