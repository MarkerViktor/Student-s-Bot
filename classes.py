import random


class User:
    def __init__(self, id, name='', surname='', group='', school='', type_of_user = 'user'):
        self.id = id
        self.name = name
        self.surname = surname
        self.study_group = group
        self.school = school
        self.type_of_user = type_of_user

    def massege_send(self, vk, message='', attachment=''):
        vk.messages.send(
            peer_id = self.id,
            message = message,
            attachment = ','.join(attachment),
            random_id = random.randint(0, 2147483647)
        )


class Chat:
    def __init__(self, id, name=''):
        self.id = id
        self.name = name
        self.official_name = name

    def massege_send(self, vk, message='', attachment=''):
        vk.messages.send(
            peer_id = self.id,
            message = message,
            attachment = ','.join(attachment),
            random_id = random.randint(0, 2147483647)
        )

