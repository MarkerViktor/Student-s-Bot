from config import *
from vk_api import keyboard
import random


def message_get(bot, peer_id, message='', attachments='', keys=''):
    vk = bot['vk']
    vk.messeges.send(
        peer_id=peer_id,
        message=message,
        attachment=','.join(attachments),
        random=random.randint(0, 9223372036854775807),
        keyboard=keys.get_keyboard()
    )

def answer_get(bot, peer_id, question='', options=''):
