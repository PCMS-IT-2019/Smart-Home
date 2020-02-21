import time
from speech.sound_cal import *

# 识别语音的参数
# 说话最大间断秒数
MAX_INTERVAL_TIME = 0.5
#百度API超时时间60秒
TIMEOUT_API = 58
#语音前后留多少空闲时间
LEISURE_TIME = 0.5
# 说话多久超时
TIMEOUT_USER = TIMEOUT_API

# 判断是否停止说话，并且在语音内添加前后空余时间
def checktalk(_is_talking):
    global is_talking,tic,tic_start,tic_stop,toc
    if tic:
        if not _is_talking and is_talking:
            if toc and round(time.time(),2) - tic_stop> MAX_INTERVAL_TIME:
                print("has Talked " + str(round(time.time(), 2) - tic_start) + "s")
                if (tic_stop == 0): print("error")
                tic,toc = False,False
                tic_start,tic_stop = 0,0
                #is_talking = False
                return False
            else:
                tic_stop = round(time.time(),2)
                toc = True
                #is_talking = True
                return True
        else:
            #is_talking = True
            return True
    elif _is_talking: # 其实这个时候肯定tic等于False
        tic = True
        tic_start = round(time.time(),2)
        #is_talking = True
        return True
    else:
        #is_talking = False
        return False

def get_talkOnce():
    p = pyaudio.PyAudio()
    global is_talking
    samp = []
    frames = []
    is_talking = False
    _is_talking = False
    i = 0
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Detecting...")
    while True:
        # 这里要添加TIMEOUT
        data = stream.read(CHUNK)
        samp.append(data)
        #samp = get_recordFrames(SAMP_TIME)
        if i == MIN_BUFFER:
            _is_talking = getAmplitude(b''.join(samp[len(samp)-1-MIN_BUFFER:])) > min_amplitude
            i = 0
        is_talking = checktalk(_is_talking)
        if(is_talking):break
        i = i + 1
    print("Start Talking")
    for i in range(0, int(RATE / CHUNK * TIMEOUT_USER)):
        frames.append(stream.read(CHUNK))
        amplitude = getAmplitude(b''.join(frames[i-int(LEISURE_TIME*RATE/CHUNK):]))
        _is_talking = amplitude > min_amplitude
        if (not checktalk(_is_talking) and amplitude != 0):
            p.terminate()
            return b''.join(samp+frames)
    p.terminate()
    return b''.join(samp+frames)

def input_loop(input_str):
    def isscalar(str):
        try:
            global temp
            temp = float(str)
        except ValueError:
            return False
        else:
            return True
    while not isscalar(input(input_str)):
        print("請輸入數字！")
    return temp