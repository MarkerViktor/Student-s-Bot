import connect as connection  # подключение к базе данных и vk.api


def start_bot():
    vk, longpoll, cursor = connection.make()
    while True:
        event = longpoll.check()  # проверяем лонгпул на новое событие
        action = event_hendler(event)  # получаем действие для нового события


def event_hendler(event):
    pass


start_bot()







