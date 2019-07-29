from config import *
from vk_api import keyboard
from classes import *
import connect
import random
bot = connect.make()


#  get
def get_attachments(attachments):
    """
    Функция возвращает список вложений в формате type+owned_id+'_'+id,
    если вложения отсутствуют, возвращает пустой список
    :param attachments:
    :return:
    """
    if len(attachments) == 0:
        return []
    items = list()
    for item in attachments:
        type = item['type']
        owner_id = item[type]['owner_id']
        id = item[type]['id']
        if 'access_key' in item[type]:
            access_key = item[type]['access_key']
            item_name = type + str(owner_id) + '_' + str(id) + '_' + str(access_key)
        else:
            item_name = type + str(owner_id) + '_' + str(id)
        items.append(item_name)
    return items


def get_answer(bot, peer_id):
    """
    Ждет ответа пользователя и возвращает текст и вложения ответа, либо первого пересланного сообщения, если оно есть.
    :param bot:
    :param peer_id: i
    """
    longpoll = bot['longpoll']
    for number in range(5):
        event = longpoll.check()
        if len(event) != 0:
            print(event)
            event = event[0].object
            if peer_id != event['from_id']:
                return 'Другое обращение'
            if len(event['fwd_messages']) != 0:
                event = event['fwd_messages'][0]
            break
    else:
        return 'Ответ не получен'
    text = event['text']
    attachments = get_attachments(event['attachments'])
    return {'text': text, 'attachments': attachments}


def make_keyboard_list(options, one_time):
    object = keyboard(one_time)
    for number in range(len(options)):
        number += 1
        if number%4 == 0:
            object.add_line()
        object.add_button()
    return object.get_keyboard()


def make_choice(bot, peer_id):
    pass

def message_send(bot, peer_id, message='', attachments='', keys=''):
    vk = bot['vk']
    vk.messeges.send(
        peer_id=peer_id,
        message=message,
        attachment=','.join(attachments),
        random=random.randint(0, 9223372036854775807),
        keyboard=keys.get_keyboard()
    )