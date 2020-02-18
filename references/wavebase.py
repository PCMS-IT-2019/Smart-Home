import math
import wave  # 调用wave模块
#import matplotlib as mpl
#mpl.use('agg')
#mpl = mpl.reload(mpl)
#import matplotlib.pyplot as plt  # 调用matplotlib.pyplot模块作为Plt
import numpy as np  # 调用numpy模块记作np

# 计算每一帧的过零率
def ZCR(frameData):
    frameNum = frameData.shape[1]
    frameSize = frameData.shape[0]
    zcr = np.zeros((frameNum, 1))

    for i in range(frameNum):
        singleFrame = frameData[:, i]
        temp = singleFrame[:frameSize-1] * singleFrame[1:frameSize]
        temp = np.sign(temp)
        zcr[i] = np.sum(temp<0)

    return zcr

# 分帧处理函数
def enframe(wavData, frameSize, overlap):
    coeff = 0.97 # 预加重系数
    wlen = len(wavData)
    step = frameSize - overlap
    frameNum:int = math.ceil(wlen / step)
    frameData = np.zeros((frameSize, frameNum))

    hamwin = np.hamming(frameSize)

    for i in range(frameNum):
        singleFrame = wavData[np.arange(i * step, min(i * step + frameSize, wlen))]
        singleFrame = np.append(singleFrame[0], singleFrame[:-1] - coeff * singleFrame[1:]) # 预加重
        frameData[:len(singleFrame), i] = singleFrame
        frameData[:, i] = hamwin * frameData[:, i] # 加窗

    return frameData


# 计算每一帧能量
def energy(frameData):
    frameNum = frameData.shape[1]
    ener = np.zeros((frameNum, 1))
    for i in range(frameNum):
        singleframe = frameData[:, i]
        ener[i] = sum(singleframe * singleframe)
    return ener

def getframeData(wavePath):
    f = wave.open(wavePath, "rb")  # 读取语音文件
    params = f.getparams()  # 返回音频参数
    nchannels, sampwidth, framerate, nframes = params[:4]  # 赋值声道数，量化位数，采样频率，采样点数
    wave_data = np.fromstring(f.readframes(nframes), dtype=np.short)
    wave_data = wave_data * 1.0 / (max(abs(wave_data)))
    print(nchannels, sampwidth, framerate, nframes)
    return enframe(wave_data,nframes,0)

def getframeData_new(wavePath):
    size = 50
    f = wave.open(wavePath, "rb")  # 读取语音文件
    nchannels, sampwidth, framerate, nframes = f.getparams()[:4]#获取音频参数
    print(nchannels, sampwidth, framerate, nframes)
    wave_data = np.fromstring(f.readframes(nframes), dtype=np.short)#获取音频数据
    wave_data_normal = wave_data * 1.0 / (max(abs(wave_data)))#归一化
    sensitivity = 0.1#选择0至1的数
    print(len(np.where(wave_data_normal>=sensitivity)[0])==0)
    first_time = (np.where(wave_data_normal>=sensitivity)[0][0]/nframes)*5
    print(first_time)

    #画图
    time = np.arange(0, nframes) * (1.0 / framerate)
    fig = plt.figure(figsize=(10, 4))
    plt.plot(time, wave_data_normal, c="g")
    plt.xlabel("time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()
