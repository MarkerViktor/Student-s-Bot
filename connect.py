import vk_api
import vk_api.bot_longpoll
import psycopg2  # работа с базами данных
from config import *  # данные для подключения к vk.api и базе данных heruko


def make():
    """Функция покдлючения к базе данных и авторизации vk_api
       Возвращает кортеж объектов vk, longpoll, cursor"""
    try:
        cursor, conn = connect_database('heroku')
    except psycopg2.ProgrammingError:
        cursor, conn = connect_database()
    except Exception:
        print("\tBase can't be connected")

    try:
        vk, longpoll = connect_vk()
        print("\tVK is connected")
    except Exception:
        print("\tVK can't be connected")

    return {'vk': vk, 'longpoll': longpoll, 'cursor': cursor, 'conn': conn}


def connect_vk():
    """Функция подключения к ВКонтакте и серверу Longpoll.
       Возвращает кортеж объектов vk и longpoll"""
    vk_session = vk_api.VkApi(token=token)
    longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id)
    return vk_session.get_api(), longpoll


def connect_database(mode=''):
    """Функция подключения к базе данных PostgrerSQL.
       Возвращает кортеж объектов cursor и conn"""
    if mode == 'heroku':
        conn = psycopg2.connect(DATABASE_host, sslmode='require')
    else:
        conn = psycopg2.connect(dbname=DATABASE_name,
                                user=DATABASE_user,
                                password=DATABASE_password,
                                host=DATABASE_host,
                                sslmode='require')
    print('\tBase is connected')
    return conn.cursor(), conn