from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import config
import classes as cl
import time
import requests

vk_session = vk_api.VkApi(token=config.token)
longpoll = VkBotLongPoll(vk_session, config.group_id)
vk = vk_session.get_api()

viktor = cl.User(94138203, name = 'Виктор', surname= 'Маркер', group='8Е81')
misha = cl.User(175750670)
while True:
    time = time.ctime(time.time()+25200)
    time = time.split(' ')[4].split(':')
    hours = time[0]
    minutes = time[1]
    response = requests.get(f'http://wttr.in/{city}', params={'format': 2, 'M': ''})
    viktor.massege_send(vk,message = response.text.strip())
    time.sleep(1850)
    #misha.massege_send(vk, message = str(random.randint(0, 1000000000)))














