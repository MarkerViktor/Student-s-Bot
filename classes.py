
import random
from vk_api.keyboard import *
from vk_api.bot_longpoll import *
class Database:
    def __init__(self, cursor,
                       conn):
        self.conn = conn
        self.cursor = cursor

    def get(self, name,
                  sort='name',
                  type='',
                  data=''):
        """

        :param name: название таблицы
        :param sort: по какому полю сортировка
        :param type: название параметра для поиска
        :param data: значение параметра для поиска
        """
        request = f'SELECT * FROM {name} '

        if data and type != '':
            request += f'WHERE {type} = '
            if isinstance(data, int):
                request += f'{data} '
            elif isinstance(data, str):
                request += f"'{data}' "

        request += f'ORDER BY {sort};'
        print(request)
        try:
            self.cursor.execute(request)
            data = self.cursor.fetchall()
            return data[0]
        except Exception:
            return 'Данные не получены'


    def add_data(self, name, data):
        """
        Метод добавление данных в указанную таблицу
        :param name:
        :param data:
        :return:
        """
        request = f'INSERT INTO {name} ('
        for item in data.keys():
            request += item + ', '
        request = request[0:len(request) - 2]
        request += ') VALUES ('
        for item in data.values():
            if isinstance(item, str):
                request += "'" + item + "'" + ', '
            if isinstance(item, int):
                request += str(item) + ', '
        request = request[0:len(request)-2]
        request += ');'
        print(request)
        try:
            self.cursor.execute(request)
            self.conn.commit()
            return 'OK'
        except Exception:
            return 'Данные не добавлены'


class Message:
    def __init__(self, vk, longpoll):
        self.vk = vk
        self.longpoll = longpoll

    def Get(self, peer_id, only_text=True):
        """
        Метод ждет сообщения от конкретного ползователя и возвращает текст и вложения или только текст
        :param peer_id:
        :param only_text:
        :return:
        """
        for number in range(7):
            event = self.longpoll.check()
            if len(event) != 0:
                event = event[0].object
                print(event)
                if 'action' in event and event['action']['type'] == 'chat_invite_user':
                    self.Send(event['peer_id'], f'ID = {event["peer_id"]} \nЧтобы использовать бота в этой беседе,впишите указанный '
                                       f'ID в таблицу, соответственно имени беседы')
                    self.Send(event['peer_id'], 'Cсылка на таблицу: https://docs.google.com/spreadsheets/d/1CB53Wri_'
                                          '0WXksMg5aRusTEfKIxzxALbt3nXarpfo8QQ/edit?usp=sharing')
                    return 'Другое обращение'
                if peer_id != event['from_id']:
                    self.Send(event['from_id'], "Student's Bot сейчас занят🙃")
                    return 'Другое обращение'
                if len(event['fwd_messages']) != 0:
                    event = event['fwd_messages'][0]
                break
        else:
            return 'Ответ не получен'
        text = event['text']
        if only_text:
            return text
        attachments = self.Get_attachments(event['attachments'])
        return {'text': text, 'attachments': attachments}

    def Get_attachments(self, attachments):
        """
        Метод возвращает кортеж из названий вложений
        Аргументом является объект attachments из сообщения
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

    def Send(self, peer_id=94138203,
                   message='',
               attachments='',
                 keyboard = ''):
        """
        :param peer_id:
        :param message:
        :param attachments:
        :param keyboard:
        :return:
        """
        return self.vk.messages.send(
            peer_id=peer_id,
            message=message,
            attachment=','.join(attachments),
            random_id=random.randint(0, 9223372036854775807),
            keyboard=keyboard
        )


class Keyboard:
    def Make(options_before: dict = [],
                    options: list = [],
              options_after: dict = {},
            options_columns: int  = 1,
                    primary: list = [],
                   negative: list = [],
                   positive: list = []):
        """

        :param options:
        :param options_after:
        :param options_columns:
        :param options_selected:
        :return:
        """
        keyboard = VkKeyboard()

        # добавление options_before
        if len(options_before) != 0:
            for option, color in options_before.items():
                keyboard.add_button(option, color)

        # добавление options
        if len(options)!=0:
            if len(options_before) != 0:
                keyboard.add_line()
            number = 0
            for option in options:
                if number%options_columns==0 and number !=0:
                    keyboard.add_line()
                if option in primary:
                    keyboard.add_button(option, 'primary')
                elif option in negative:
                    keyboard.add_button(option, 'negative')
                elif option in positive:
                    keyboard.add_button(option, 'positive')
                else:
                    keyboard.add_button(option, 'default')
                number += 1

        # добавление options_after
        if len(options_after) != 0:
            if len(options) != 0:
                keyboard.add_line()
            for option, color in options_after.items():
                keyboard.add_button(option, color)

        return keyboard.get_keyboard()

begin_keyboard = Keyboard.Make(options=['Начать'])
