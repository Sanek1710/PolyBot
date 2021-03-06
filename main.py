import datetime
import json
import time

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

import vk_message
from usermngr import UserManager
from vk_message import Message


def main():

    with open('auth_data.json', 'r', encoding='utf-8') as user_data_file:
        auth_data = json.load(user_data_file)

    vk_session = vk_api.VkApi(token=auth_data["group_token"])

    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session, preload_messages=True)
    user_manager = UserManager()
    
    print('[PolyBot:START]')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                message = vk.messages.get_by_id(message_ids=event.message_data['id'])["items"][0]
                message = vk_message.load(message)
                print (message.dump())

                user = user_manager[message.from_id]
                msg = user.cmdhandler.handle(message, vk)

                if msg:
                    for uid in user_manager.ids(include_admin=True):
                        user = user_manager[uid]
                        user.cmdhandler.handle(msg, vk)

            except Exception as e:
                print('[main]', e)

    print('[PolyBot:STOP]')


if __name__ == '__main__':
    while True:
        try:
            try:
                main()
            except Exception as e:
                print('[PolyBot:Exception] ', e, end='\r')
            time.sleep(10)

        except KeyboardInterrupt as k:
            print('[PolyBot:BREAK]')
            break
    