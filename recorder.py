import os
import time
import wave  # 调用wave模块
import numpy as np  # 调用numpy模块记作np
from misc import *
from const import *

min_amplitude = 0
is_talking,tic,toc = False,False,False
tic_stop = 0

#如果秒数等于0，则获取最短语音数据
def get_recordFrames(seconds):
    #print("* recording")
    # 打开数据流
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 关闭数据流
    stream.stop_stream()
    stream.close()
    #print("* done recording")
    return b''.join(frames)

# 保存语音为.pcm
def save_recordFrames(filename,frames):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(frames)
    wf.close()

# 是否标定
def iscalibrated():
    return os.path.exists(WAVE_OUTPUT_FILENAME)

# 校正时的录音长度
# 灵敏度
# 返回判断为有声音的最小振幅
def calibrate(sensitivity):
    # 获取语音
    if(os.path.isfile(WAVE_OUTPUT_FILENAME)):
        print("找到標定音頻")
        f = wave.open(WAVE_OUTPUT_FILENAME, "rb")  # 读取语音文件
        nchannels, sampwidth, framerate, nframes = f.getparams()[:4]  # 获取音频参数
        wave_data = f.readframes(nframes)
        global RECORD_SECONDS,RATE
        RATE = framerate
        RECORD_SECONDS = nframes/framerate
    else:
        wave_data = get_recordFrames(RECORD_SECONDS)
    # 转换语音数据格式
    wave_data = np.fromstring(wave_data, dtype=np.short)
    # 记录语音，每次打开只需输入灵敏度
    save_recordFrames(WAVE_OUTPUT_FILENAME, wave_data)
    # 归一化
    wave_data_normal = wave_data * 1.0 / (max(abs(wave_data)))
    #灵敏度判断
    filter = np.where(wave_data_normal >= 1-sensitivity)
    if len(filter[0]) != 0:
        # 找到最小值的索引
        min_index = filter[0][np.argmin(wave_data[filter])]
        # 半秒的采样点数
        half_seconds_frames = RATE*0.5
        # 取灵敏度之中最小值的半秒内
        if(min_index-half_seconds_frames/2<0):
            half = wave_data[0:int(min_index+half_seconds_frames)]
        elif(min_index+half_seconds_frames/2>wave_data.size):
            half = wave_data[int(wave_data.size-half_seconds_frames):wave_data.size]
        else:
            half = wave_data[int(min_index-half_seconds_frames/2):int(min_index+half_seconds_frames/2)]
        # 均值
        global min_amplitude
        min_amplitude = wave_data[min_index]#np.mean(np.abs(half))/2
        return min_amplitude
    else:
        print("靈敏度太低，檢測不到你正在說話，退出程序重試")
        return 0

# 获取振幅
def getAmplitude(frames):
    if(len(frames) < MIN_BUFFER*CHUNK):
        return 0
    else:
        amplitude = np.max(np.abs(np.fromstring(frames, dtype=np.short)))
        print(amplitude)
        return amplitude

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
    global is_talking
    samp = []
    frames = []
    is_talking = False
    _is_talking = False
    i = 0
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Detecting...")
    while True:
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
            return b''.join(samp+frames)
    return b''.join(samp+frames)

def quit():
    p.terminate()

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