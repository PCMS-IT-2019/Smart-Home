from aip import AipSpeech

""" APPID AK SK """
APP_ID = '17956963'
API_KEY = 'y9umW9TaYizYaT6CyU08Bblv'
SECRET_KEY = 'NMGN6AnQoYE357VKY6Q6e9VzV0sdACtO'

#create接口
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 讀取文件function
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 獲取audio中的test.pcm,
response = client.asr(get_file_content('./audio/test.wav'), 'wav', 16000, {
    'dev_pid': 1536,
})

#print response
print(response)