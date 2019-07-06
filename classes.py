import random
class User:
    def __init__(self, id, name='', surname='', group='', school='', specialty=''):
        self.id = id
        self.name = name
        self.surname = surname
        self.group = group
        self.school = school
        self.specialty = specialty

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

    def massege_send(self, vk, message='', attachment=''):
        vk.messages.send(
            peer_id = self.id,
            message = message,
            attachment = ','.join(attachment),
            random_id = random.randint(0, 2147483647)
        )

