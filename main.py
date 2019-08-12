import time
from config import *
from classes import *
import connect


def Start():
    global BOT
    BOT = connect.make()
    while True:
        events = BOT.Listen(quantity=0)
        for event in events:
            event = event.object
            id = event['from_id']
            
            if BOT.UserVerification(event):
                BOT.OtherUserHandler(event)
                continue
            if BOT.ExtraEventHandler(event):
                continue
            try:
                mode = Mode(id)
                print(mode)
                if mode == 'Управление':
                    control = Control(id)
                    if control == 'Добавить пользователя':
                        AddUser(id)
                    elif control == 'Добавить беседу':
                        AddChat(id)
                    elif control == 'Список разрешенных пользователей':
                        UsersList(id)

                raise End
            except End:
                BOT.MessageSend(id, 'Завершено', keyboard=KeyboardMake({'Начать': 'default'})[0])
            except Timeout:
                BOT.MessageSend(id, 'Время ожидания истекло', keyboard=KeyboardMake({'Начать': 'default'})[0])


def Mode(id):
    keyboard, buttons = KeyboardMake(
        options = {
            'Управление': 'default'
        },
        options_after={
            'Завершить': 'negative'
        }
    )
    BOT.MessageSend(id, 'Выберите раздел', keyboard=keyboard)
    while True:
        answer = BOT.AnswerGet(id)
        if answer not in buttons:
            BOT.MessageSend(id, 'Используйте кнопки')
        else:
            return answer


def Control(id):
    keyboard, buttons = KeyboardMake(
        options = {
            'Добавить пользователя': 'primary',
            'Добавить беседу': 'primary',
            'Список разрешенных пользователей': 'default'
        },
        options_after={
            'Завершить': 'negative'
        }
    )
    BOT.MessageSend(id, 'Выберите функцию', keyboard=keyboard)
    while True:
        answer = BOT.AnswerGet(id)
        if answer not in buttons:
            BOT.MessageSend(id, 'Используйте кнопки')
        else:
            return answer


def AddUser(id):
    BOT.MessageSend(id, 'Укажите ссылку на страницу пользователя',
                 keyboard=KeyboardMake({'Отмена': 'negative'})[0])
    BOT.MessageSend(id, 'Чтобы одновременно добавить нескольких пользователей, в одном сообщении '
                          'разместите несколько ссылок (каждая на новой строке)')
    answer = BOT.AnswerGet(id)
    if '.com/' in answer:
        links = answer.split('\n')
        for link in links:
            try:
                user = BOT.UserGet(link)
                name = user['full_name']
                user_id = user['id']
                BOT.DataAdd('users', {'name': name, 'id': user_id})
                BOT.MessageSend(id, f'{name} c ID = {user_id} успешно внесён в БД')
            except Exception:
                BOT.MessageSend(id, 'Неверный формат входных данных, попробуйте снова')
                continue
                
        keyboard, buttons = KeyboardMake(
            options_before={'Добавить': 'default'},
            options_after={'Завершить': 'positive'}
        )
        BOT.MessageSend(id, 'Добавить еще?', keyboard=keyboard)
        answer = BOT.AnswerGet(id)
        if answer == 'Добавить':
            AddUser(id)


    else:
        BOT.MessageSend(id, 'Неверный формат входных данных')
        AddUser(id)


def AddChat(id):
    BOT.MessageSend(id, 'Чтобы использовать бота для новой беседы:')
    BOT.MessageSend(id, '— Пригласите бота в беседу с помощью кнопки на стене сообщества бота')
    BOT.MessageSend(id, '— Следуйте указаниям бота в сообщении, пришедшем в беседу сразу после приглашения')


def UsersList(id):
    users = dict(BOT.DataGet('users', 'name')).values()
    users_list = ''
    for number in range(len(users)):
        users_list += f'{number+1} — {users[number]}\n'

    BOT.MessageSend(id, 'Разрешенные пользователи:\n' + users_list)


Start()