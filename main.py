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
                ControlAddUser(id)
            elif control == 'Добавить беседу':
                ControlAddChat(id)
            elif control == 'Список разрешенных пользователей':
                ControlUsersList(id)

        elif mode == 'Рассылка':
            mailing = Mailing(id)
            if mailing == 'Моментальная рассылка':
                MailingMoment(id)
            elif mailing == 'Отложенная рассылка':
                pass
            elif mailing == 'Редактировать/удалить':
                pass

        raise End

    except End:
        BOT.MessageSend(id, 'Завершено', keyboard=KeyboardMake({'Начать': 'default'})[0])

    except Timeout:
        BOT.MessageSend(id, 'Время ожидания истекло', keyboard=KeyboardMake({'Начать': 'default'})[0])




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


def ControlAddUser(id):
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
                BOT.MessageSend(id, f'{name} c ID = {user_id} успешно внесён(а) в БД')
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


def ControlUsersList(id):
    # Показать список разрешенных пользователей
    users = list(dict(BOT.DataGet('users', 'name')).values())
    list_of_strings = list()
    string = 0
    for number in range(len(users)):
        if number%100 == 0:
            if number != 0:
                string += 1
            list_of_strings.append('')
        list_of_strings[string] += f'{number+1} — {users[number]}\n'
    BOT.MessageSend(id, 'Разрешенные пользователи:')
    for string in list_of_strings:
        BOT.MessageSend(id, string)



def ControlAddChat(id):
    # Добавление беседы
    BOT.MessageSend(id, 'Чтобы использовать бота для новой беседы:')
    BOT.MessageSend(id, '— Пригласите бота в беседу с помощью кнопки на стене сообщества бота')
    BOT.MessageSend(id, '— Следуйте указаниям бота в сообщении, пришедшем в беседу сразу после приглашения')



def Mailing(id):
    # Рассылка
    keyboard, buttons = KeyboardMake(
        options={
            'Моментальная рассылка': 'primary',
            'Отложенная рассылка': 'default',
            'Редактировать/удалить (last 24 h)': 'default',
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


def MailingMoment(id):
    # Моментальная рассылка
    message = MailingMassageGet(id)

def MailingMassageGet(id):
    mailing = Message()
    keyboard, buttons = KeyboardMake(

        options_before={
            'Просмотр': 'default'
        },
        options_after={
            'Отмена': 'negative'
        }
    )
    BOT.MessageSend(id, 'Отправьте сообщение с рассылаемыми текстом и вложениями или перешлите чужое '
                        'сообщение, содержащее их', keyboard=keyboard)
    while True:
        pass

Start()