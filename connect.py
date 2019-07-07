import vk_api
from vk_api.bot_longpoll import VkBotLongPoll as vk_api_bot
import config
import psycopg2


def make():
    """Функция покдлючения к базе данных и авторизации vk_api
       Возвращает список объектов vk, longpoll, cursor"""
    try:
        cursor = connect_base('heroku')
    except psycopg2.ProgrammingError:
        cursor = connect_base()
    except Exception:
        print("Base can't be connected")

    try:
        vk, longpoll = connect_vk()
    except Exception:
        print("VK can't be connected")
    return vk, longpoll, cursor


def connect_vk():
    vk_session = vk_api.VkApi(token=config.token)
    longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, config.group_id)
    return vk_session.get_api(), longpoll


def connect_base(mode=''):
    if mode == 'heroku':
        conn = psycopg2.connect(config.DATABASE_host, sslmode='require')
    else:
        conn = psycopg2.connect(dbname=config.DATABASE_name,
                                user=config.DATABASE_user,
                                password=config.DATABASE_password,
                                host=config.DATABASE_host,
                                sslmode='require')
    print('Base is connected')
    return conn.cursor()