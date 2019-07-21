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
    bot['cursor'].execute('SELECT * FROM {0};'.format(table_name))
    return dict(bot['cursor'].fetchall())


def add_to_database(bot, table_name, data):
    """Функция добавляет заданную строку в указанную таблицу активной базы данных"""
    try:
        query = "INSERT INTO {0} VALUES ({1} , {2});".format(table_name, "'"+data[1]+"'", str(data[0]))
        print(query)
        bot['cursor'].execute(query)
        bot['conn'].commit()
        print('Запись', data, 'добавлена в таблицу', table_name)
    except Exception:
        print('Запись', data, 'не добавлена в таблицу', table_name)


def add_chat_to_database(bot, peer_id, from_id):
    """Функция добавления id и name беседы ВК в базу данных groups,
       при приглашении бота в беседу"""
    print('Спрашиваю имя группы')
    answer = answer_get(bot, from_id, 'Укажите официльное имя учебной группы (организации)' 
                                      'в ответном сообщении вида:\n"8Е81" или "Профорги"')
    if answer != None:
        name = answer['text'].upper()
        data = (peer_id, name)
        add_to_database(bot, 'groups', data)
    else:
        message_send(bot, from_id, 'Название группы не получено, '
                                   'исключите бота из беседы и повторите процедуру добавления')
        print('Имя не получено')
        return None


def get_tasks():
    return []


def message_send(bot, peer_id, message='', attachment=''):
    """Функция отправки сообщения конкретному пользователю"""
    bot['vk'].messages.send(
        peer_id=peer_id,
        message=message,
        attachment=','.join(attachment),
        random_id=random_id()
    )


def attachments_get(attachments):
    """Функция озвращает список вложений в формате type+owned_id+'_'+id,
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