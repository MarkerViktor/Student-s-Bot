import connect as connection  # подключение к базе данных и vk.api
from functions import *
import time


def start_bot():
    bot = connection.make()
    while True:
        Time = time.ctime(time.time())
        tasks = get_tasks()  # получаем запланиролванные задания из БД
        if len(tasks) != 0:
            print('Есть запланированные задания')
            for task in tasks:
                task_performer(bot, task)
        else:
            print(Time)
            event = bot['longpoll'].check()  # проверяем лонгпул на новое событие
            if len(event) != 0:
                event = event[0].object
                print(Time, 'Обрабатываю событие\n', event)
                event_handler(bot, event)


def event_handler(bot, event):
    """Функция главного обработчика событий бота"""
    peer_id = event['peer_id']
    from_id = event['from_id']
    text = event['text']
    attachments = attachments_get(event['attachments'])

    print('Событие от {0} в диалоге {1} (текст: "{2}", вложений: {3})'.format(from_id, peer_id, text, len(attachments)))

    #  Событие добавления бота в беседу
    if 'action' in event and event['action']['type'] == 'chat_invite_user':
        print('Приглашение в беседу', peer_id, 'от', from_id)
        add_chat_to_database(bot, peer_id, from_id)
        return None





def task_performer(bot, task):
    """Функция обработки запланированного события"""
    pass


start_bot()









