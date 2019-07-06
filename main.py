from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import config
import classes as cl
import requests
import time
import psycopg2

conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
print(conn)
vk_session = vk_api.VkApi(token=config.token)
longpoll = VkBotLongPoll(vk_session, config.group_id)
vk = vk_session.get_api()

viktor = cl.User(94138203, name = 'Виктор', surname= 'Маркер', group='8Е81')
misha = cl.User(175750670)

while True:
    time0 = time.ctime(time.time()+25200)
    time1 = time0.split(' ')[4].split(':')
    hours = time1[0]
    minutes = time1[1]
    seconds = time1[2]
    if int(hours) == 7 and int(minutes) == 0 and int(seconds) == 0:
        response = requests.get("http://wttr.in/Томск", params={'format':2, 'M': ''})
        viktor.massege_send(vk,message = 'Погода в Томске:\n' + response.text.strip())
    #misha.massege_send(vk, message = str(random.randint(0, 1000000000)))














