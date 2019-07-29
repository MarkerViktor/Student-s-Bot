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
            if handler(bot, event) == 'ОК':
                message_send(bot, event['from_id'], 'Завершено')


def handler(bot, event):
    """Функция главного обработчика событий бота"""
    peer_id = event['peer_id']
    from_id = event['from_id']

    type = command_type(bot, event)
    if type == 'Добавление в беседу':
        print("Добавление в беседу")
        return add_chat_to_database(bot, from_id, peer_id)
    elif type == 'Рассылка':
        return mailing_get(bot, peer_id)


def command_type(bot, event):
    peer_id = event['peer_id']
    if 'action' in event and event['action']['type'] == 'chat_invite_user':
        return 'Добавление в беседу'
    else:
        return choice_generator(bot, peer_id, 'Выберите', ['Рассылка',
                                                           'Добавить беседу'
                                                           'Добавить пользователя'])


bot_start()









