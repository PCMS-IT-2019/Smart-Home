#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from time import sleep
from aip import AipSpeech
from numpy import frombuffer,short

import wave
#from wave import open  #这样写就重名了
from pyaudio import PyAudio,paInt16
#import pyaudio
from threading import Thread
import pygame
import os
import tkinter



#由于百度语音识别最大时长为60s，所以我们创建这个计时的方法，然后在子线程中调用
timeout = False

def timeclock():
	global timeout
	timeout = True
	#循环里面的全局变量要加global
	for x in range(60):
		print('ticking...', timeout)
		sleep(1)
		#如果标志位为False，则停止计时
		if timeout == False:
			return 0
	#超过60秒赋值为false，停止录音
	timeout = False
	


#录音
def my_record(path = '01.wav'):
	#规定声音属性
	framerate=16000				#采样频率
	NUM_SAMPLES=2000			#内部缓存块的大小，每次读取的采样数据块的个数
	channels=1					#声道
	sampwidth=2					#采样大小/采样宽度/位深2B 16bit

	pa=PyAudio()
	#创建输入流
	stream=pa.open(format = paInt16,channels=1,
		rate=framerate,input=True,
		frames_per_buffer=NUM_SAMPLES)
	#help(stream)
	Buf_Data=[]
	'''
	#定时录制语音模式， 录音时间公式：1/频率*采样点数*20 = 1/16000*2000*20 = 2.5s
	for count in range(20):
		string_audio_data = stream.read(NUM_SAMPLES)
		#print(string_audio_data, '\n')
		#将录制的数据存放到数组中
		Buf_Data.append(string_audio_data)
		print('....')
	'''

#按需录音模式，连续2.5秒不出声，就停止录音
#测试：		
	#datalistfile = ''
	coutif = 0
	print('正在聆听.....')
	#计时功能启动
	tc = Thread(target = timeclock, name = 'loopwall')
	tc.deamon = True
	tc.start()
#刚开始录音的时候可能有比较长的时间做准备，所以我们先录制1.25秒钟
	for xtime in range(10):
		string_audio_data = stream.read(NUM_SAMPLES)
		Buf_Data.append(string_audio_data)
		print('..')
#一般人这时候已经开始说话了
	#当没超时录音
	global timeout
	while timeout:
		#循环一圈用时约0.125s
		string_audio_data = stream.read(NUM_SAMPLES)
		Buf_Data.append(string_audio_data)
		print('..')
		#将数据转换为数组
		data_list = frombuffer(string_audio_data, dtype=short)
		#判断是否有声音
		if max(data_list)<5000:		#5000:分贝阈值，小于5000视为环境噪音或静音
			coutif += 1
		else:
			coutif = 0
		#如果连续15个采样点都小于5000，退出循环，即连续1/16000*2000*15=1.875秒没声，就不录音了
		if coutif > 15:
			timeout = False
			break
	


	#将存储的数据保存成wav文件
	wf=wave.open(path,'wb')	#注意，文件名中不能带：等特殊符号
	#设置声道、采样频率、采样大小
	wf.setnchannels(channels)
	wf.setsampwidth(sampwidth)
	wf.setframerate(framerate)
	wf.writeframes(b"".join(Buf_Data))
	wf.close()
	stream.close()

	


#chunk=2014
#播放wav文件
def play_wav(path = '01.wav'):
	wf=wave.open(path,'rb')
	
	p=PyAudio()
	#创建输出流
	stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
	wf.getnchannels(),rate=wf.getframerate(),output=True)
	while True:
		#读取波形数据
		data=wf.readframes(wf.getnframes())
		#print(data)
		if data==b"":	#注意数据是字节型的，所以必须加b
			break
		#将声音写进输出流进行播放
		stream.write(data)

	stream.close()
	p.terminate()
	return 0

#语音识别方法
def speech_recog(filePath = '01.wav'):
	#初始化百度语音模块
	#这里面的KEY是我自己在百度ai平台上申请的，请各位大侠不要泄露，感恩！
	APP_ID = '15650993'
	API_KEY = 'Ln3tGvXgULhSiv84edVhmx00'
	SECRET_KEY = 'jfKMKA5OQ2Nk1rwZ7LCbDdP4ytop8Zt5'
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	with open(filePath, 'rb') as fp:
		data = fp.read()   		
	#调用百度语音识别功能并返回处理 结果：{'corpus_no': '6663056022087844625', 'err_msg': 'success.', 'err_no': 0, 'result': ['你好，百度语音。'], 'sn': '413216893291551363622'} 
	recog_str = client.asr(data, 'wav', 16000, {'dev_pid': 1537,})
	try:
		return recog_str['result'][0]
	except:
		print('声音过于嘈杂或网络波动，请重新尝试')

#语音合成方法
def art_speech(speech_Info = '这里是百度语音合成'):
	#初始化百度语音模块
	#这里面的KEY是我自己在百度ai平台上申请的，请各位大侠不要泄露，感恩！
	APP_ID = '15650993'
	API_KEY = 'Ln3tGvXgULhSiv84edVhmx00'
	SECRET_KEY = 'jfKMKA5OQ2Nk1rwZ7LCbDdP4ytop8Zt5'
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	result = client.synthesis(speech_Info, 'zh', 4, {'spd':3, 'pit':5,'vol':5})

# 识别正确返回语音二进制 错误则返回dict
	if not isinstance(result, dict):
		with open('baiduad.mp3', 'wb') as f:
			f.write(result)
		#播放mp3文件
		sleep(0.2)
		pygame.mixer.init()
		pygame.mixer.music.load('baiduad.mp3')
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy():
			pygame.time.delay(500)
		pygame.mixer.music.stop()



def speech_main():
	global button
	button['text'] = '正在聆听'
	#录音
	my_record()
	#语音识别
	s = speech_recog()
	button['text'] = '点击开始说话'
	text.delete(1.0, 'end')
	text.insert(tkinter.INSERT, str(s))
	global timeout
	timeout = False
	print('timeout: ',timeout)


	#播放刚才的录音
	#play_wav()
	#print(type(s))
	if str(s) == '关机。':

		speech_Info = '宝宝先睡了，债见'
		art_speech(speech_Info)
		os.system('shutdown -s')



def start_speech_main():
	t = Thread(target = speech_main)
	t.deamon = True
	t.start()
	




if __name__ == '__main__':

	#创建主窗口
	win = tkinter.Tk()
	#设置标题
	win.title('百度语音模块')
	#设置大小和位置
	#win.geometry('400x400+200+0')
	#在win窗口放置一个框
	frm1 = tkinter.Frame(win)
	frm1.grid(row = 0, column = 0)
	button = tkinter.Button(frm1, text = '点击开始说话', command = start_speech_main,
		width = 10,
		height = 2)
	button.pack()

	frm2 = tkinter.Frame(win)
	frm2.grid(row = 1, column = 0)
	#创建滚动条
	scroll = tkinter.Scrollbar(frm2)
	#文本控件，用于显示多行文本
	#创建文本框
	text = tkinter.Text(frm2, height = 6, width = 30)
	#设置滚动条和文本框显示方式
	scroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)  #右侧显示，并且填充Y轴
	text.pack(side = tkinter.LEFT, fill = tkinter.Y)
	#关联文本框和滚动条的位置关系
	scroll.config(command = text.yview)    #滚动条的位置控制文本在Y轴移动
	text.config(yscrollcommand = scroll.set)
	text.insert(tkinter.INSERT, '欢迎使用语音识别')


	win.mainloop()

