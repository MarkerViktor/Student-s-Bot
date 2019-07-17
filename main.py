import connect as connection  # подключение к базе данных и vk.api
from functions import *
from vk_api.bot_longpoll import  VkBotEventType


talks = dict()


def start_bot():
    vk, longpoll, cursor = connection.make()
    while True:
        tasks = get_tasks()  # получаем запланиролванные задания из БД
        if len(tasks) != 0:
            task_performer(tasks)
        else:
            event = longpoll.check()  # проверяем лонгпул на новое событие
            if len(event) != 0:
                event_handler(event[0])


def event_handler(event):
    print(event.object)
    peer_id = event.object['peer_id']
    from_id = event.object['from_id']
    message_text = event.object['text']
    message_attachments = attachments_get(event.object['attachments'])
    print(peer_id, from_id, message_text, message_attachments)



def task_performer(task):
    pass


start_bot()







