import time
from config import *
from classes import *
import connect


def Start():
    global VK, DATABASE, USERS
    VK, DATABASE = connect.make()
    USERS = DATABASE.UsersUpdate()
    print(USERS)
    while True:
        event = VK.Listen(0)
        id = event['from_id']
        if id not in USERS:
            other_users_handler(id)
            continue

        if VK.ExtraEventHandler(event):
            continue
        try:
            mode = Mode(id)
            print(mode)
            if mode == 'Добавить пользователя':
                AddUser(id)
            elif mode == 'Добавить беседу':
                AddChat(id)
            raise End
        except End:
            VK.MessageSend(id, 'Завершено', keyboard=KeyboardMake({'Начать': 'default'})[0])
        except Timeout:
            VK.MessageSend(id, 'Время ожидания истекло', keyboard=KeyboardMake({'Начать': 'default'})[0])


def Mode(id):
    keyboard, buttons = KeyboardMake(
        options = {
            'Добавить пользователя': 'default',
            'Добавить беседу': 'default'
        },
        options_after={
            'Завершить': 'negative'
        }
    )
    VK.MessageSend(id, 'Выберите функцию', keyboard=keyboard)
    while True:
        answer = VK.MessageGet(id)
        if answer not in buttons:
            VK.MessageSend(id, 'Используйте кнопки')
        else:
            return answer


def AddUser(id):
    VK.MessageSend(id, 'Укажите ссылку на страницу пользователя',
                 keyboard=KeyboardMake({'Отмена': 'negative'})[0])
    VK.MessageSend(id, 'Чтобы одновременно добавить нескольких пользователей, в одном сообщении '
                          'разместите несколько ссылок (каждая на новой строке)')
    answer = VK.MessageGet(id)
    if '.com/' in answer:
        links = answer.split('\n')
        for link in links:
            try:
                user = VK.UserGet(link)
                name = user['full_name']
                user_id = user['id']
                DATABASE.DataAdd('users', {'name': name, 'id': user_id})
                VK.MessageSend(id, f'{name} c ID = {user_id} успешно внесён в БД')
            except Exception:
                VK.MessageSend(id, 'Неверный формат входных данных, попробуйте снова')
                continue
        UsersUpdate()
        keyboard, buttons = KeyboardMake(
            options_before={'Добавить': 'default'},
            options_after={'Завершить': 'positive'}
        )
        VK.MessageSend(id, 'Добавить еще?', keyboard=keyboard)
        answer = VK.MessageGet(id)
        if answer == 'Добавить':
            AddUser(id)

    else:
        VK.MessageSend(id, 'Неверный формат входных данных')
        AddUser(id)

def AddChat(id):
    VK.MessageSend(id, 'Чтобы использовать бота для новой беседы:')
    VK.MessageSend(id, '— Пригласите бота в беседу с помощью кнопки на стене сообщества бота')
    VK.MessageSend(id, '— Следуйте указаниям бота в сообщении, пришедшем в беседу сразу после приглашения')


def other_users_handler(id):
    VK.MessageSend(id, 'Доступ запрещен ⛔', keyboard=KeyboardMake({'Начать': 'default'})[0])


def UsersUpdate():
    print('UsersUpdate')
    global USERS
    global DATABASE
    USERS = DATABASE.UsersUpdate()

Start()