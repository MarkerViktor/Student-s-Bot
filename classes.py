from random import *
from vk_api.keyboard import VkKeyboard

class Bot:

    def __init__(self, vk, longpoll, cursor, conn):
        self.vk = vk
        self.longpoll = longpoll
        self.cursor = cursor
        self.conn = conn

    def MessageSend(self, id=0, message: str='', attachments: list='', keyboard='', ids=[], object: dict ={}):
        """
        :param id:
        :param message:
        :param attachments:
        :param keyboard:
        :return:
        """
        id, message, attachments, keyboard = id, message, attachments, keyboard
        if len(object) != 0:
            if 'id' in object.keys():
                id = object['id']

            if 'text' in object.keys():
                message = object['text']

            if 'attachments' in object.keys():
                attachments = object['attachments']

            if 'keyboard' in object.keys():
                keyboard = object['keyboard']

            if 'ids' in object.keys():
                ids = object['ids']

        try:
            if len(ids) == 0:
                return self.vk.messages.send(
                    peer_id = id,
                    message = message,
                    attachment = ','.join(attachments),
                    keyboard = keyboard,
                    random_id = randint(0, 9223372036854775807)
                )
            else:
                messages = list()
                for id in ids:
                    messages.append(self.vk.messages.send(
                        peer_id=id,
                        message=message,
                        attachment=','.join(attachments),
                        keyboard=keyboard,
                        random_id=randint(0, 9223372036854775807)
                    ))
                    return messages

        except Exception as x:
            print('MessageSend Error', x)

    def AnswerGet(self, id, only_text=True):
        """
        :param id:
        :param only_text:
        :return:
        """
        event = self.Listen()

        if self.UserVerification(event):
            return self.AnswerGet(id, only_text)

        if self.ExtraEventHandler(event):
            return self.AnswerGet(id, only_text)

        if self.UserCheck(event, id):
            return self.AnswerGet(id, only_text)

        if only_text:
            text = event['text']
            if text == 'Отмена' or text == 'Завершить':
                raise End
            return text
        attachments = self.AttachmentsGet(event['attachments'])
        text = event['text']
        return {'text': text, 'attachments': attachments}

    def AttachmentsGet(self, attachments):
        """
        :param attachments:
        :return:
        """
        if len(attachments) == 0:
            return []
        items = list()
        for item in attachments:
            type = item['type']
            owner_id = item[type]['owner_id']
            id = item[type]['id']
            if 'access_key' in item[type]:
                access_key = item[type]['access_key']
                item_name = type + str(owner_id) + '_' + str(id) + '_' + str(access_key)
            else:
                item_name = type + str(owner_id) + '_' + str(id)
            items.append(item_name)
        return items

    def UserGet(self, link='', id_or_screen_name=''):
        """
        :param link:
        :param id_or_screen_name:
        :return:
        """
        """Метод получения объекта пользователя"""
        #  link — ссылка на страницу пользователя
        #  id_or_screen_name — id или ник пользователя
        if link != '':
            try:
                user = link.split('.com/')[1]
                if user.startswith('id') and user.split('id')[1].isdigit():
                    id = user.split('id')[1]
                    person = self.vk.users.get(user_ids=id)[0]
                else:
                    person = self.vk.users.get(user_ids=user)[0]
            except Exception:
                return 'Error'
        if id_or_screen_name != '':
            try:
                person = self.vk.users.get(user_ids=id_or_screen_name, lang=ru)[0]
            except Exception:
                return 'Error'

        person['full_name'] = person['last_name'] + ' ' + person['first_name']
        person.pop('is_closed')
        person.pop('can_access_closed')
        return person

    #event
    def Listen(self, quantity=5):
        if quantity != 0:
            for a in range(quantity):
                event = self.longpoll.check()
                if len(event) != 0:
                    event = event[0].object


                    print(event)
                    return event
            raise Timeout
        else:
            while True:
                event = self.longpoll.check()
                if len(event) != 0:
                    print(event)
                    return event

    def ExtraEventHandler(self, event):
        peer_id = event['peer_id']
        from_id = event['from_id']
        if peer_id != from_id:
            if 'action' in event and event['action']['type'] == 'chat_invite_user':
                print('Добавление в беседу')
                self.MessageSend(peer_id, f'ID = {peer_id} \nЧтобы использовать бота в этой беседе, '
                'впишите указанный ID в таблицу, соответственно имени беседы')
                self.MessageSend(peer_id, 'Cсылка на таблицу: https://docs.google.com/spreadsheets/d/1CB53Wri_'
                                      '0WXksMg5aRusTEfKIxzxALbt3nXarpfo8QQ/edit?usp=sharing')
            return True
        return False

    def UserVerification(self, event):
        id = event['from_id']
        user = self.DataGet('users', select_type='id', select_data=id)
        if len(user) == 0:
            self.OtherUserHandler(event)
            return True
        else:
            return False

    def UserCheck(self, event, id):
        peer_id = event['peer_id']
        from_id = event['from_id']
        if peer_id != id and from_id != id:
            self.MessageSend(from_id, 'Бот сейчас занят, обратись позже)')
            return True
        return False

    #database
    def DataGet(self, table_name, sort='', select_type='', select_data=''):
        """
        :param table_name:
        :param sort:
        :param select_type:
        :param select_data:
        :return:
        """
        """Получение данных из БД"""
        #         name — имя таблицы
        #         sort — имя столбца, по ктоторому производится сортировка
        #  select_type — имя столбца, по которому производится поиск
        #  select_data — значение поля, искомых строк
        request = f'SELECT * FROM {table_name} '

        if select_data and select_type != '':
            request += f'WHERE {select_type} = '
            if isinstance(select_data, int):
                request += f'{select_data}'
            elif isinstance(select_data, str):
                request += f"'{select_data}'"
        if sort != '':
            request += f'ORDER BY {sort};'
        else:
            request += ';'
        print(request)
        try:
            self.cursor.execute(request)
            data = self.cursor.fetchall()
            return data
        except Exception as f:
            print(f)
            return 'Error'

    def DataAdd(self, table_name, data):
        """Добавление данных в БД"""
        #  table_name
        request = f'INSERT INTO {table_name} ('
        for item in data.keys():
            request += str(item) + ', '
        request = request[0:len(request) - 2]
        request += ') VALUES ('
        for item in data.values():
            if isinstance(item, str):
                request += "'" + item + "'" + ', '
            if isinstance(item, int):
                request += str(item) + ', '
        request = request[0:len(request) - 2]
        request += ');'
        print(request)
        try:
            self.cursor.execute(request)
            self.conn.commit()
            return 'OK'
        except Exception:
            return 'Error'

    # other user handler
    def OtherUserHandler(self, event):
        id = event['from_id']
        self.MessageSend(id, 'Нет доступа ⛔')


class Message():

    def __init__(self, ids=[], text='', attachments = []):
        self.text = text
        self.attachments = attachments
        self.ids = ids

    def Get(self):
        return {
            'text': self.text,
            'attachments': self.attachments,
            'ids': self.ids
        }





class Timeout(Exception):
    def __init__(self):
        print('TIMEOUT')

class End(Exception):
    def __init__(self):
        pass





def KeyboardMake(options_before: dict = {}, options: dict or list = {},
                 options_after: dict = {}, options_columns: int  = 1):
    """Создание клавиатуры с обределенными кнопками"""
    #  options_before — словарь с кнопками первой строки, где ключи — это label, а значения — color
    #  options — словарь или список с оновным блоком кнопок, где ключи — это label, а значения — color
    #  options_after — словарь с кнопками последней строки, где ключи — это label, а значения — color
    #  options_columns — количество столбцов в блоке options
    keyboard = VkKeyboard()

    buttons = list(options_before.keys()) + list(options_after.keys())

    # превращаем список options в словарь со значениями 'default'
    if isinstance(options, list) or isinstance(options, set):
        buttons += options
        labels = options
        options = dict()
        for label in labels:
            options[label] = 'default'
    else:
        buttons += list(options.keys())

    # добавление options_before
    if len(options_before) != 0:
        for label, color in options_before.items():
            if color in ['default', 'negative', 'positive', 'primary']:
                keyboard.add_button(label, color)
            else:
                keyboard.add_button(label, 'default')

    # добавление options
    if len(options)!=0:
        if len(options_before) != 0:
            keyboard.add_line()
        number = 0
        for label, color in options.items():
            if number%options_columns==0 and number !=0:
                keyboard.add_line()
            if color in ['default', 'negative', 'positive', 'primary']:
                keyboard.add_button(label, color)
            else:
                keyboard.add_button(label, 'default')
            number += 1

    # добавление options_after
    if len(options_after) != 0:
        if len(options) != 0 or len(options_before) != 0:
            keyboard.add_line()
        for label, color in options_after.items():
            if color in ['default', 'negative', 'positive', 'primary']:
                keyboard.add_button(label, color)
            else:
                keyboard.add_button(label, 'default')

    return keyboard.get_keyboard(), buttons


