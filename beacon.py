from aip import AipSpeech
import time
import schedule
import os
import sys
import datetime
import wave
import numpy as np
import pygame
from pygame.locals import *
from pydub import AudioSegment
import requests

HEFENG_API_KEY = 'xxxxxxxxxx'


perdict = {
                #0:'小美',
                4:'丫丫',
                5118:'小鹿',
                103:'米朵',
                110:'小童',
                111:'小萌',
                4119:'小鹿',
                4105:'灵儿',
                #4117:'小乔',
                4100:'小雯',
                4103:'米朵',
                4144:'姗姗',
                4278:'小贝',
                #4140:'小新',
                4254:'小清'}
codes = np.array(list(perdict.keys()))
names = np.array(list(perdict.values()))
random_index = np.random.choice(len(codes))
random_code = codes[random_index]
random_name = names[random_index]

bgms = [
    'bgm01.wav'
    'bgm02.wav'
]
bgm = np.random.choice(bgms)


# 初始化
def getText():

    # '%Y-%m-%d %H:%M:%S' 获取时间的年月日 时分秒
    hour = datetime.datetime.now().strftime('%H')
    #text='现在是北京时间'+str(now)+'时。'
    now  = time.localtime()

    text = '现在是北京时间' + str(hour) + '时。我的名字是，' + random_name +  '，'

    if now.tm_hour < 5 and  now.tm_hour >= 2:
        text += '凌晨好！'
    elif now.tm_hour >= 5 and now.tm_hour < 9:
        text += '早上好！'
    elif now.tm_hour >= 9 and now.tm_hour < 11:
        text += '上午好！'
    elif now.tm_hour >= 11 and now.tm_hour < 14:
        text += '中午好！'
    elif now.tm_hour >= 14 and now.tm_hour < 19:
        text += '下午好！'
    elif (now.tm_hour >= 19 and now.tm_hour < 24) or (now.tm_hour >= 0 and now.tm_hour < 2):
        text += '晚上好！'

    #text += '连接每一份热爱，共享每一刻通联！这里是，四九城无线，接收频率：439MHz，下差：8，大红门中继，发射哑音：118.8！'
    text += '这里是，四九城无线，接收频率：439MHz，下差：8，大红门中继，发射哑音：118.8！'
    text += '石景山中继，发射哑音：100！沙河中继，发射哑音：123！永清中继，发射亚音：203.5！丰体中继维护中！通州中继维护中！'


    #  获取天气预报
    forecast_weather = get_forecast_weather('101010100')
    if forecast_weather:
        #day = forecast_weather['daily'][0];
        #text += f"今天天气，白天{day['textDay']}，夜间{day['textNight']}，最高{day['tempMax']}℃，最低{day['tempMin']}℃'。"
        day = forecast_weather['daily'][1];
        text += f"明天天气，白天{day['textDay']}，夜间{day['textNight']}，最高{day['tempMax']}℃，最低{day['tempMin']}℃'。"
        #day = forecast_weather['daily'][2];
        #text += f"后天白天{day['textDay']}，夜间{day['textNight']}，最高温度{day['tempMax']}℃，最低温度{day['tempMin']}℃'。"
    else:
        print("获取天气数据失败！")

    # 获取当前的温度值
    #realtime_weather = get_realtime_weather('101010100')
    #forecast_weather = get_forecast_weather('101010100')
    #if realtime_weather and forecast_weather:
    #    print(f"实时天气：{realtime_weather['now']['text']}，温度：{realtime_weather['now']['temp']}℃")
    #    print("未来三天天气预报：")
    #    for day in forecast_weather['daily']:
    #        print(f"{day['fxDate']}：白天{day['textDay']}，夜间{day['textNight']}，最高温度{day['tempMax']}℃，最低温度{day['tempMin']}℃")
    #else:
    #    print("获取天气数据失败")

    #text+='嘿，宝贝们，今天天气好好呀，阳光像金色的小精灵，偷偷溜进了我们的窗户。快点起床，一起去公园找小蝴蝶玩耍吧！它们的翅膀一闪一闪的，好像在对我们眨眼睛呢。还有好多好多漂亮的花儿，红的、黄的、粉的，像彩虹掉在了地上。别忘了带上你的小零食，我们一起分享快乐，让这个美好的一天变成最甜蜜的回忆哦！' 
    text += random_name + '，祝各位通联愉快！73！'
    print(text)
    return text

def get_realtime_weather(location):
    url = "https://m53byf4kh2.re.qweatherapi.com/v7/weather/now"
    params = {
        "key": HEFENG_API_KEY,
        "location": location
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None

def get_forecast_weather(location):
    url = "https://m53byf4kh2.re.qweatherapi.com/v7/weather/3d"
    params = {
        "key": HEFENG_API_KEY,
        "location": location
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None


def tts(weather):
    """ 你的 APPID AK SK """
    APP_ID = '88888'
    API_KEY = 'xxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxx'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(weather,'zh', 1, {
        'vol': 15,  #音量，取值0-15，默认为5中音量
        'per': random_code,   #发音人  发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
        'spd': 4, #语速    语速，取值0-9，默认为5中语速
        'aue': 6
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    #print(result)
    if not isinstance(result, dict):
        with open('/home/baoyang/audio.wav', 'wb') as f:
            f.write(result)
            time.sleep(1)
            f.close()
            timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(timelog + ' 语音合成完毕')

def mixBgm():
    # 读取mp3的波形数据
    sound = AudioSegment.from_file('audio.mp3', format = 'MP3')
    bgm = AudioSegment.from_file('audio.mp3', format = 'MP3')
    combined = sound.overlay(bgm)
    combined.export('result.mp3', format='mp3')
    print('背景音乐混音完毕')

def play():
    try:
        pygame.init()
        #pygame.mixer.init(frequency=44100)
        pygame.mixer.init(frequency=48000)
        sound1 = pygame.mixer.Sound('/home/baoyang/audio.wav')
        pygame.mixer.music.load('/home/baoyang/' + bgm)
        timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(timelog + ' 开始播放背景音乐：' + bgm + '...')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.0)
        pygame.time.delay(4000)
        pygame.mixer.music.set_volume(0.7)
        pygame.time.delay(1000)
        pygame.mixer.music.set_volume(0.4)
        pygame.time.delay(1000)
        pygame.mixer.music.set_volume(0.1)
        pygame.time.delay(1000)
        timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(timelog + ' 开始播放语音...')
        channel = sound1.play()
        sound1.set_volume(1.0)
        while channel.get_busy():
            pygame.time.delay(100)
            pass
        pygame.mixer.music.set_volume(1.0)
        timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(timelog + ' 语音播放已停止...')
        #pygame.mixer.music.set_volume(0.5)
        #pygame.time.delay(1000)
        pygame.time.delay(1000)
        #timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(timelog + ' 淡出开始...')
        #pygame.mixer.music.fadeout(5000)
        pygame.time.delay(1000)
        pygame.mixer.music.set_volume(0.7)
        pygame.time.delay(2000)
        pygame.mixer.music.set_volume(0.4)
        pygame.time.delay(1000)
        #pygame.mixer.music.fadeout(10000)
        pygame.mixer.music.set_volume(0.1)
        pygame.time.delay(1000)
        pygame.mixer.music.set_volume(0.05)
        pygame.time.delay(1000)
        timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(timelog + ' 播报完毕')
    finally:
        pygame.mixer.quit()
        pygame.quit()

def job():
    #r = True
    #argn = len(sys.argv)
    #if argn > 1:
    #    arg = str(sys.argv[1])
    #    if arg == '-p':
    #        r = False

    #if r:
    #    timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #    delay = np.random.randint(3*60, 10*60)
    #    print(timelog + ' 等待' + str(delay) + '秒后启动播报...')
    #    time.sleep(delay)

    timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timelog + ' ============播报启动=============')

    weather=getText()
    tts(weather)
    play()

    timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timelog + ' ============播报结束=============')

job()

#timelog = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#delay = np.random.randint(20*60, 40*60)
#print(timelog + ' 等待' + str(delay) + '秒后再次播报...')
#time.sleep(delay)

#job()