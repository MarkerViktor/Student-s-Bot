import random
import vk_api
import vk_api.bot_longpoll
import psycopg2  # работа с базами данных
import time
from config import *
from classes import *


def random_id():
    return random.randint(0, 2147483647)


def message_send(bot, peer_id, message='   ', attachments=''):
    """Функция отправки сообщения конкретному пользователю
    :param bot:
    :param peer_id:
    :param message:
    :param attachments:
    """
    attachment = ','.join(attachments),
    try:
        bot['vk'].messages.send(
            peer_id=peer_id,
            message=message,
            attachment=attachment,
            random_id=random_id()
        )
    except Exception:
        bot['vk'].messages.send(
            peer_id=peer_id,
            message='  \n\t',
            attachment=attachment,
            random_id=random_id()
        )


def answer_get(bot, id, message=''):

    """Функция вопрос-ответ.
       При ответе от объекта, которому задан вопрос, возвращает объект события vk_api;
       при ответе от другого пользователя или по истечению 10 time-out'ов возвращает None
       :param bot:
       :param id:
       :param message:
       :return: """
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
            raise NoAnswer


def tasks_get():
    return []


def data_get(bot, table_name):
    """Функция возвращает заданную таблицу из активной базы данных
    :param bot:
    :param table_name:
    :return:
    """
    bot['cursor'].execute('SELECT name, id FROM {0} ORDER BY name;'.format(table_name))
    return dict(bot['cursor'].fetchall())


def attachments_get(attachments):
    """Функция возвращает список вложений в формате type+owned_id+'_'+id,
       если вложения отсутствуют, возвращает пустой список
       :param attachments:
       :return: """
    if len(attachments) == 0:
        return []
    items = list()
    for item in attachments:
        type = item['type']
        owner_id = item[type]['owner_id']
        access_key = item[type]['access_key']
        id = item[type]['id']
        item_name = type + str(owner_id) + '_' + str(id) + '_' + str(access_key)
        items.append(item_name)
    return items


def select_chats(bot, peer_id, groups):
    """Возвращает список имен чатов, выбраных пользователем
    :param bot:
    :param peer_id:
    :param groups:
    :return:
    """
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


def add_to_database(bot, table_name, data):
    """Функция добавляет заданную строку в указанную таблицу активной базы данных
    :param bot:
    :param table_name:
    :param data:
    :return:
    """
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
       при приглашении бота в беседу
       :param bot:
       :param peer_id:
       :param from_id:
       :return: """
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


def mailing_get(bot, peer_id):
    """Функция рассылки сообщений
    :param bot:
    :param peer_id:
    :return:
    """
    groups = data_get(bot, 'groups')
    chats = select_chats(bot, peer_id, groups)
    if chats == None:
        return None

    message_send(bot, peer_id,'Вы выбрали:\n — '+'\n — '.join(chats))


    message = answer_get(bot, peer_id, 'Отправьте сообщение с текстом и вложениями для рассылки или перешлите  другое '
                                       'сообщение, содержащее в себе текст и вложения')
    if message == None:
        return None


    if len(message['fwd_messages'])>0:
        message = message['fwd_messages'][0]
    if 'reply_message' in message:
        message = message['reply_message']


    attachments = attachments_get(message['attachments'])
    text = message['text']
    print('\n',attachments,'\n',text)

    message_send(bot, peer_id, text, attachments)

    confirmation = answer_get(bot, peer_id, 'Осуществить рассылку?\n'
                                            '(Пришлите "12345", чтобы подтвердить)')
    if confirmation['text'] == '12345':
        for chat in chats:
            message_send(bot, groups[chat], text, attachments)
        return 'Рассылка произведена'


