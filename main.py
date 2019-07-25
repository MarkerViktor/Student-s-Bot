import connect as connection  # подключение к базе данных и vk.api
from functions import *
import time


def bot_start():
    bot = connection.make()
    Bot(bot)


def Bot(bot):
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
                handler(bot, event)


def handler(bot, event):
    """Функция главного обработчика событий бота"""
    peer_id = event['peer_id']
    from_id = event['from_id']
    text = event['text']

    print('Обращение от {0} в диалоге {1} (текст: "{2}")'.format(from_id, peer_id, text))

    #  Событие добавления бота в беседу
    if 'action' in event and event['action']['type'] == 'chat_invite_user':
        print('Приглашение в беседу', peer_id, 'от', from_id)
        add_chat_to_database(bot, peer_id, from_id)
        return None
    if len(text) > 0:
        result = handler_2(bot, peer_id)
        if result == None:
            print('Обращение не обработано')
            message_send(bot, peer_id, 'Обращение не обработано')
        else:
            print('Обращение обработано')


def handler_2(bot, peer_id):
    command = answer_get(bot, peer_id, 'Выберите функцию:\n'
                                       '1 — Сделать рассылку;\n'
                                       '2 — ...')
    if command == None:
        return None
    text = command['text']

    print('Команда', text)
    if text == '1':
        print('Рассылка')
        return mailing_get(bot, peer_id)
    else:
        print('Неверная команда')
        message_send(bot, peer_id, 'Неверная команда, попробуйте снова')
        handler_2(bot, peer_id)



def task_performer(bot, task):
    """Функция обработки запланированного события"""
    pass


bot_start()









