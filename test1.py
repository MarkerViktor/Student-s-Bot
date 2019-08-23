from config import *
import connect
from classes import *
import vk_api
import vk_api.longpoll
from vk_api.longpoll import VkEventType
bot = connect.make()

vk_session=vk_api.vk_api.VkApi(token=token)
api = vk_session.get_api()

items = api.messages.getConversationMembers(
    peer_id = 2000000000 + 104
)['items']
for item in items:
    id = item['member_id']
    user = api.users.get(user_ids=id)[0]
    name =  user['last_name'] + ' ' + user['first_name']
    print(name, id)
    print(bot.DataAdd('users',{'id': id, 'name': name}))

