import vk_api
import vk_api.bot_longpoll
import time
import psycopg2  # работа с базами данных
from config import *  # данные для подключения к vk.api и базе данных heruko
from classes import Bot


def make():
    """Функция покдлючения к базе данных и авторизации vk_api
       Возвращает словарь с ключами vk, longpoll, cursor"""
    try:
        try:
            cursor, conn = connect_database('heroku')
        except Exception as e:
            cursor, conn = connect_database()

        vk, longpoll = connect_vk()
        print("\tVK and Database is connected")
    except Exception as e:
        print("\tVK and Database can't be connected", e)
        time.sleep(5)
        return make()
    bot = Bot(vk, longpoll, cursor, conn)
    return bot


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