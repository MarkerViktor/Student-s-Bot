from vk_api import vk_api, keyboard
import connect
import random

vk = connect.make()['vk']
key = keyboard.VkKeyboard()
for q in range(10):
    for w in range(4):
        key.add_button(label='_')
    if q<9:
        key.add_line()




vk.messages.send(
    peer_id = 94138203,
    message = 'Привет',
    keyboard = key.get_keyboard(),
    random_id = random.randint(0, 2147483647)
)
