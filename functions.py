import random
import vk_api
import vk_api.bot_longpoll
import psycopg2  # работа с базами данных
import time
from config import *


def random_id():
    return random.randint(0, 2147483647)


def data_get(cursor, table_name, data, search_value):
    cursor.execute('SELECT ' + ', '.join(data) + ' FROM ' + table_name + ' WHERE id = ' + search_value)
    return cursor.fetchall()


def attachments_get(attachments):
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


def get_tasks():
    return []


def massege_send(vk, message='', attachment=''):
    vk.messages.send(
        peer_id=id,
        message=message,
        attachment=','.join(attachment),
        random_id=random.randint(0, 2147483647)
    )

