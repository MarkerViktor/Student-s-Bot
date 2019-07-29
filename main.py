import connect as connection  # подключение к базе данных и vk.api
from functions import *
from classes import *
import time


def bot_start():
    bot = connection.make()
    Bot(bot)


def Bot(bot):
    while True:
        Time = time.ctime(time.time())
        event = bot['longpoll'].check()  # проверяем лонгпул на новое событие
        if len(event) != 0:
            event = event[0].object
            print(Time, 'Обрабатываю событие\n', event)
            handler(bot, event)


def handler(bot, event):
    """Функция главного обработчика событий бота"""
    peer_id = event['peer_id']
    from_id = event['from_id']
    if peer_id != from_id:
        return 0

    #  Событие добавления бота в беседу
    if 'action' in event and event['action']['type'] == 'chat_invite_user':
        try:
            add_chat_to_database(bot, peer_id, from_id)
        except NoAnswer:
            message_send(bot, peer_id, '')

    if text != '':
        command = answer_get(bot, peer_id, 'Выберите функцию:\n'
                                           '1 —  Рассылка;')
        if command == None:
            return None
        text = command['text']
        try:
            if text == '1':
                try:
                    mailing_get(bot, peer_id)
                except NoAnswer:
                    message_send(bot, peer_id, '')

            else:
                message_send(bot, peer_id, 'Неверная команда, попробуйте снова')
                handler(bot, event)





def task_performer(bot, task):
    """Функция обработки запланированного события"""
    pass


bot_start()









