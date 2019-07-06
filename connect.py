import vk_api
from vk_api.bot_longpoll import VkBotLongPoll as vk_api_bot
import config
import psycopg2


def start():
    """Функция покдлючения к базе данных и авторизации vk_api."""
    vk_session = vk_api.VkApi(token=config.token)
    longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, config.group_id)
    try:
        conn = psycopg2.connect(config.DATABASE_host, sslmode='require')
        print('Base is connected')
    except psycopg2.ProgrammingError:
        conn = psycopg2.connect(dbname=config.DATABASE_name,
                                user=config.DATABASE_user,
                                password=config.DATABASE_password,
                                host=config.DATABASE_host)
        print('Base is connected')
    else:
        print("Can't become connected")
    vk = vk_session.get_api()
    cursor = conn.cursor()
    return {'vk': vk, 'longpoll': longpoll, 'cursor': cursor}
