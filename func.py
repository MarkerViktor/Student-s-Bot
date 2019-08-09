from config import *
from vk_api.keyboard import VkKeyboard
from classes import *
import connect
import random


def make_choice(peer_id,
                question,
                options):
    """
    :param bot:
    :param peer_id:
    :param question:
    :param options:
    :return: Список наименований, выбраных пользователем; "Ответ не получен" или "Выход"
    """

    Message.Send(peer_id, question)

    choice = list()
    keyboard = Keyboard.Make(
        options=options,
        options_columns=4,
        options_selected=choice,
        items_before=[{'Выбрать ВСЕ': 'primary',
                       'Начать сначала': 'default'}],
        items_after=[{'Выход': 'negative',
                      'Подтвердить': 'positive'}],
    )
    Message.Send(peer_id, '(Чтобы выбрать\отменить элементы, просто нажимайте на них)', keyboard=keyboard)


    while True:
        text = Message.Get(peer_id)

        if text not in options:

            if text == 'Ответ не получен': # NoAnswer
                Message.Send(peer_id, 'Время ожидания истекло', keyboard=VkKeyboard().get_empty_keyboard())
                return 'Ответ не получен'

            elif text == '':
                continue

            elif text == 'Подтвердить':
                if len(choice) == 0:
                    Message.Send(peer_id, 'Ничего не выбрано')
                    continue
                break

            elif text == 'Выход':  # Выход
                Message.Send(peer_id, '😉', keyboard=VkKeyboard().get_empty_keyboard())
                return 'Выход'

            elif text == 'Начать сначала':
                choice = list()

            elif text == 'Выбрать ВСЕ':
                choice = list(options)

            else:
                Message.Send(peer_id, 'Используйте кнопки')
                continue

        else:
            if text not in choice:
                choice.append(text)
            else:
                choice.remove(text)
        keyboard = Keyboard.Make(
            options=options,
            options_columns=4,
            options_selected=choice,
            items_before=[{'Выбрать ВСЕ': 'primary',
                           'Начать сначала': 'default'}],
            items_after=[{'Выход': 'negative',
                          'Подтвердить': 'positive'}],
        )
        Message.Send(peer_id, '😉', keyboard=keyboard)
    print(choice)
    Message.Send(peer_id, 'Вы выбрали \n —'+'\n —'.join(choice))
    Message.Send(peer_id, '😉', keyboard=VkKeyboard().get_empty_keyboard())
    return(choice)



#f = ['8Е81','8Е82','8Т81','8Т82','8К81','8К82','8И81','8И82', '8В81', '8В82', '4П81', '2У92']
#make_choice(admin_id,'Выберите группы для рассылки', f)
#print(list)

