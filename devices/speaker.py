from devices.playsound import *
from speech.stream import *
from devices.playsound import playsound

def speak(audio):
    # 一定要保存为.mp3格式
    filename = 'speech/audio/speak.mp3'
    with open(filename,"wb") as f:
        f.write(audio)
    #save_recordFrames(filename, audio, FORMAT=pyaudio.paInt32)
    '''Linux尚未测试，可能会出现权限不足的可能'''
    p = playsound()
    p.play(filename)
    p.stop()
    p.close()