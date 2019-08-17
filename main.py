import time
from config import *
from classes import *
import connect

#  изменить механику работы выхода из программы и добавления логов
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
            GeneralHandler(id)



def GeneralHandler(id):
    try:
        mode = Mode(id)
        print(mode)
        if mode == 'Управление':
            control = Control(id)
            print(control)
            if control == 'Добавить пользователя':
                AddUser(id)
            elif control == 'Добавить беседу':
                AddChat(id)
            elif control == 'Список разрешенных пользователей':
                UsersList(id)

        elif mode == 'Рассылка':
            mailing = Mailing(id)
            if mailing == 'Моментальная рассылка':
                pass
            elif mailing == 'Отложенная рассылка':
                pass
            elif mailing == 'Редактировать/удалить':
                pass
        BOT.AddLog(id, mode, True)
        raise End

    except End:
        BOT.MessageSend(id, 'Завершено', keyboard=KeyboardMake({'Начать': 'default'})[0])

    except Timeout:
        BOT.MessageSend(id, 'Время ожидания истекло', keyboard=KeyboardMake({'Начать': 'default'})[0])

    except Exception:
        BOT.MessageSend(id, 'Завершено', keyboard=KeyboardMake({'Начать': 'default'})[0])


def Mode(id):
    # Главное меню
    keyboard, buttons = KeyboardMake(
        options = {
            'Рассылка': 'default',
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
    # Управление
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
            return answer ## #


def AddUser(id):
    # Добавление пользователя
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


def UsersList(id):
    # Показать список разрешенных пользователей
    users = list(dict(BOT.DataGet('users', 'name')).values())
    users_list = ''
    for number in range(len(users)):
        users_list += f'{number+1} — {users[number]}\n'

    BOT.MessageSend(id, 'Разрешенные пользователи:\n' + users_list)


def AddChat(id):
    # Добавление беседы
    BOT.MessageSend(id, 'Чтобы использовать бота для новой беседы:')
    BOT.MessageSend(id, '— Пригласите бота в беседу с помощью кнопки на стене сообщества бота')
    BOT.MessageSend(id, '— Следуйте указаниям бота в сообщении, пришедшем в беседу сразу после приглашения')



def Mailing(id):
    # Рассылка
    keyboard, buttons = KeyboardMake(
        options={
            'Моментальная рассылка': 'primary',
            'Отложенная рассылка': 'primary',
            'Редактировать/удалить (last 24 h)': 'primary',
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


Start()