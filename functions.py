import random
import vk_api
import vk_api.bot_longpoll
import psycopg2  # работа с базами данных
import time
from config import *


def answer_get(bot, id, message=''):

    """Функция вопрос-ответ.
       При ответе от объекта, которому задан вопрос, возвращает объект события vk_api;
       при ответе от другого пользователя или по истечению 10 time-out'ов возвращает None"""
    if message != '':
        message_send(bot, id, message)
    time = 0
    while True:
        time += 1
        print('time = ', time)
        answer_event = bot['longpoll'].check()
        if len(answer_event) != 0:

            peer_id = answer_event[0].object['peer_id']
            if peer_id == id:
                return answer_event[0].object
            else:
                message_send(bot, peer_id, "Student's Bot сейчас занят")
        if time == 10:
            return None


def random_id():
    return random.randint(0, 2147483647)


def data_get(bot, table_name):
    """Функция возвращает заданную таблицу из активной базы данных"""
    bot['cursor'].execute('SELECT * FROM {0} ORDER BY name;'.format(table_name))
    return dict(bot['cursor'].fetchall())


def add_to_database(bot, table_name, data):
    """Функция добавляет заданную строку в указанную таблицу активной базы данных"""
    try:
        query = "INSERT INTO {0} VALUES ('{1}' , {2});".format(table_name, data[0], str(data[1]))
        print(query)
        bot['cursor'].execute(query)
        bot['conn'].commit()
        print('Запись', data, 'добавлена в таблицу', table_name)
        return True
    except Exception:
        print('Запись', data, 'не добавлена в таблицу', table_name)
        return False


def add_chat_to_database(bot, peer_id, from_id):
    """Функция добавления id и name беседы ВК в базу данных groups,
       при приглашении бота в беседу"""
    print('Спрашиваю имя группы')
    answer = answer_get(bot, from_id, 'Укажите официльное имя учебной группы (организации) ' 
                                      'в ответном сообщении вида:\n"8Е81" или "Профорги"')
    if answer == None:
        message_send(bot, from_id, 'Название группы не получено, '
                                   'исключите бота из беседы и повторите процедуру добавления')
        print('Имя не получено')
        return False

    name = answer['text'].upper()
    data = (name, peer_id)

    if add_to_database(bot, 'groups', data):
        message_send(bot, from_id, 'Беседа добавлена в базу данных')
        return True
    else:
        message_send(bot, from_id, 'Ошибка добавления беседы в базу данных.\nИсключите бота из беседы и повторите процедуру добавления')
        return False


def get_tasks():
    return []


def message_send(bot, peer_id, message='   ', attachment=''):
    """Функция отправки сообщения конкретному пользователю"""
    bot['vk'].messages.send(
        peer_id=peer_id,
        message=message,
        attachment=','.join(attachment),
        random_id=random_id()
    )

def mailing_get(bot, peer_id):
    """Функция рассылки сообщений"""
    groups = data_get(bot, 'groups')
    chats = select_chats(bot, peer_id, groups)
    if chats == None:
        return None
    message_send(bot, peer_id,'Вы выбрали:\n — '+'\n — '.join(chats))

    message = answer_get(bot, peer_id, 'Пришлите сообщение для рассылки\n'
                                       'Изображения должны находиться в одном из ваших альбомов')
    print(message)
    attachments = attachments_get(message['attachments'])

    text = message['text']
    if len(text) == 0:
        text = '  '
    print(attachments,'\n',text)

    message_send(bot, peer_id, text, attachments)
    if answer_get(bot, peer_id, 'Осуществить рассылку по указанным группам?\n'
                                '(Пришлите "12345", чтобы подтвердить)')['text'] == '12345':
        for chat in chats:
            message_send(bot, groups[chat], text, attachments)
        return 'OK'



def select_chats(bot, peer_id, groups):
    """Возвращает список имен чатов, выбраных пользователем"""
    text_list = ('В ответном сообщении перечислите цифры напротив выбираемых групп через пробел или "все", ' 
                'если требуется выбрать все группы\n')
    number = 0
    for group in groups.keys():
        text_list += str(number) + ' — ' + group + '\n'
        number += 1
    answer = answer_get(bot, peer_id, text_list)
    if answer == None:
        return None
    else:
        try:
            answer = answer['text']
            if answer.lower().strip() == 'все':
                return groups.keys()
            answer = answer.split(' ')
            chat_numbers = list()
            for num in answer:
                if int(num)<len(groups):
                    num.strip()
                    chat_numbers.append(int(num))
            names = list()
            number = 0
            for group in groups.keys():
                for num in chat_numbers:
                    if num == number:
                        names.append(group)
                number += 1
            return names
        except Exception:
            message_send(bot, peer_id, 'Неверено выбраны группы')
            print('Неверно выбраны группы')
            return select_chats(bot, peer_id, groups)


def attachments_get(attachments):
    """Функция возвращает список вложений в формате type+owned_id+'_'+id,
       если вложения отсутствуют, возвращает пустой список"""
    if len(attachments) == 0:
        return []
    items = list()
    for item in attachments:
        type = item['type']
        owner_id = item[type]['owner_id']
        id = item[type]['id']
        item_name = type + str(owner_id)+'_'+str(id)
        items.append(item_name)
    return items