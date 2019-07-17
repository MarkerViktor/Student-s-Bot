import vk_api
import vk_api.bot_longpoll
import psycopg2  # работа с базами данных
from config import *  # данные для подключения к vk.api и базе данных heruko


def make():
    """Функция покдлючения к базе данных и авторизации vk_api
       Возвращает кортеж объектов vk, longpoll, cursor"""
    try:
        cursor = connect_database('heroku')
    except psycopg2.ProgrammingError:
        cursor = connect_database()
    except Exception:
        print("\tBase can't be connected")

    try:
        vk, longpoll = connect_vk()
        print("\tVK is connected")
    except Exception:
        print("\tVK can't be connected")

    return vk, longpoll, cursor


def connect_vk():
    vk_session = vk_api.VkApi(token=token)
    longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id)
    return vk_session.get_api(), longpoll


def connect_database(mode=''):
    if mode == 'heroku':
        conn = psycopg2.connect(DATABASE_host, sslmode='require')
    else:
        conn = psycopg2.connect(dbname=DATABASE_name,
                                user=DATABASE_user,
                                password=DATABASE_password,
                                host=DATABASE_host,
                                sslmode='require')
    print('\tBase is connected')
    return conn.cursor()