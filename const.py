# 参数文件，用户可自行调整
from enum import Enum

class DEV_PID(Enum):
    CN_MIX = 1536
    CN_ONLY = 1537
    EN = 1737
    CANTON = 1637

""" APPID AK SK """
APP_ID = '17956963'
API_KEY = 'y9umW9TaYizYaT6CyU08Bblv'
SECRET_KEY = 'NMGN6AnQoYE357VKY6Q6e9VzV0sdACtO'

# 识别语音的参数
# 说话最大间断秒数
MAX_INTERVAL_TIME = 0.5
#百度API超时时间60秒
TIMEOUT_API = 58
#语音前后留多少空闲时间
LEISURE_TIME = 0.5
# 说话多久超时
TIMEOUT_USER = TIMEOUT_API