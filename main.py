import connect as connection  # подключение к базе данных и vk.api
from func import *
from classes import *
import time


def bot_start():
    global bot
    try:
        bot = connection.make()
    except Exception:
        time.sleep(5)
        bot_start()
    global Message
    Message = Message(bot['vk'], bot['longpoll'])
    global Database
    Database = Database(bot['cursor'], bot['conn'])
    Bot(bot)



def Bot(bot):
    while True:
        Time = time.ctime(time.time())
        event = bot['longpoll'].check()  # проверяем лонгпул на новое событие
        if len(event) != 0:
            event = event[0].object
            print(Time + ' Обрабатываю событие\n'+ str(event))
            result = handler(event)
            if result == 'OK':
                Message.Send(event['from_id'], 'Завершено успешно', keyboard=VkKeyboard.get_empty_keyboard())
            elif result == 'Ответ не получен':
                Message.Send(event['from_id'], 'Время ожидания истекло', keyboard=VkKeyboard.get_empty_keyboard())


def handler(event):
    """Функция главного обработчика событий бота"""
    peer_id = event['peer_id']
    from_id = event['from_id']


    if peer_id != from_id:
        if 'action' in event and event['action']['type'] == 'chat_invite_user':
            Message.Send(peer_id, f'ID = {peer_id} \nЧтобы использовать бота в этой беседе, '
                                   'воспользуйтесь функцией "Добавить беседу в БД"')
        else:
            return 'Событие из беседы'


    mode = get_mode(event)
    if mode == 'Ответ не получен':
        return mode
    if mode == 'Добавить пользователя\беседу в БД':
        result = add_chat_or_user(peer_id) #  добавление пользователя или чата в базу данных
        return result
    elif mode == 'Рассылка':
        result = mailing(peer_id) #  рассылка
        return result


def get_mode(event):

    peer_id = event['from_id']

    options = ['Добавить пользователя\беседу в БД']
    keyboard = Keyboard.Make(options = options, positive=['Рассылка'])
    Message.Send(peer_id, 'Выберите функцию', keyboard=keyboard)
    while True:
        answer = Message.Get(peer_id)
        if answer == 'Ответ не получен':
            return answer
        elif answer not in options:
            Message.Send(peer_id, 'Используйте кнопки')
        else:
            return answer


def add_chat_or_user(peer_id):
    options = ['Пользователь']
    keyboard = Keyboard.Make(options = options)
    Message.Send(peer_id, message='Кого (что) вы хотите добавить в базу данных бота?', keyboard=keyboard)
    while True:
        answer = Message.Get(peer_id)
        if answer == 'Ответ не получен':
            return answer
        elif answer not in options:
            Message.Send(peer_id, 'Используйте кнопки')
        elif answer == 'Пользователь':
            result = add_user(peer_id)
            return result
        elif answer == 'Беседа':
            result = add_chat(peer_id)
            return result


def add_user(peer_id):
    Message.Send(peer_id, 'Укажите ссылку на страницу пользователя',
                 keyboard=VkKeyboard.get_empty_keyboard())
    Message.Send(peer_id, 'Чтобы одновременно добавить нескольких пользователей, в одном сообщении '
                          'разместите несколько ссылок (каждая на новой строке)')
    answer = Message.Get(peer_id)
    try:
        answer = answer.split('\n')
        for user in answer:
            user = user.split('.com/')[1]
            if user.startswith('id') and user.split('id')[1].isdigit():
                id = user.split('id')[1]
                user = bot['vk'].users.get(user_ids=user)[0]
                user = user['first_name'] + ' ' + user['last_name']
            else:
                user = bot['vk'].users.get(user_ids=user)[0]
                id = user['id']
                user = user['first_name'] + ' ' + user['last_name']
            Database.add_data('users', {'id': int(id)})
            Message.Send(peer_id, user + ' c id = ' + str(id) + ' добавлен(а) в БД')
        return 'OK'

    except Exception:

        Message.Send(peer_id, 'Неверная форма ответа')
        return add_user(peer_id)


def add_chat(peer_id):
    pass


def mailing(peer_id):
    return 'OK'
bot_start()









