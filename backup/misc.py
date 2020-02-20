import pyaudio
# 录音
# 创建PyAudio对象
p = pyaudio.PyAudio()
# 定义数据流块
CHUNK = 2000#1024
FORMAT = pyaudio.paInt16
CHANNELS = 1#2
RATE = 16000

#最短需要5个buffer才有能成为二进制语音
MIN_BUFFER = 4
#单线程下的参数
#采样时间
SAMP_TIME = 0.5

# 标定
# 要写入的文件名
WAVE_OUTPUT_FILENAME = "calibration.pcm"
# 标定录音时间
RECORD_SECONDS = 5

# 调试
DEBUG = False




