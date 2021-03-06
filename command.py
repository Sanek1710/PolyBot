import sqlite3
from queue import Queue

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import taskmngr
from taskmngr import Answer, Task
from vk_message import Message

USER_KEYBOARD = VkKeyboard(one_time=False, inline=False)
USER_KEYBOARD.add_button('/почты', color=VkKeyboardColor.POSITIVE)
USER_KEYBOARD.add_button('/ссылки', color=VkKeyboardColor.POSITIVE)
USER_KEYBOARD.add_line()
USER_KEYBOARD.add_openlink_button('/диск',
        link='https://drive.google.com/drive/folders/1JnDu4QvpLZbxnZ8w4Spt998eOa0tJ-RE?usp=sharing')
USER_KEYBOARD.add_openlink_button('/расписание', 
        link='https://ruz.spbstu.ru/faculty/122/groups/30725')
USER_KEYBOARD.add_line()
USER_KEYBOARD.add_button('/задачи', color=VkKeyboardColor.PRIMARY)
USER_KEYBOARD.add_button('/taskinfo', color=VkKeyboardColor.PRIMARY)


ADMIN_KEYBOARD = VkKeyboard(one_time=False, inline=False)
ADMIN_KEYBOARD.add_button('/почты', color=VkKeyboardColor.POSITIVE)
ADMIN_KEYBOARD.add_button('/ссылки', color=VkKeyboardColor.POSITIVE)
ADMIN_KEYBOARD.add_line()
ADMIN_KEYBOARD.add_openlink_button('/диск',
        link='https://drive.google.com/drive/folders/1JnDu4QvpLZbxnZ8w4Spt998eOa0tJ-RE?usp=sharing')
ADMIN_KEYBOARD.add_openlink_button('/расписание', 
        link='https://ruz.spbstu.ru/faculty/122/groups/30725')
ADMIN_KEYBOARD.add_line()
ADMIN_KEYBOARD.add_button('/задачи', color=VkKeyboardColor.PRIMARY)
ADMIN_KEYBOARD.add_button('/taskinfo', color=VkKeyboardColor.PRIMARY)
ADMIN_KEYBOARD.add_line()
ADMIN_KEYBOARD.add_button('/forall', color=VkKeyboardColor.PRIMARY)
ADMIN_KEYBOARD.add_button('/forfew', color=VkKeyboardColor.PRIMARY)
ADMIN_KEYBOARD.add_line()
ADMIN_KEYBOARD.add_button('/newtask', color=VkKeyboardColor.PRIMARY)
ADMIN_KEYBOARD.add_button('/exitadmin', color=VkKeyboardColor.NEGATIVE)


class CommandHandler:
    def __init__(self, uid, user_manager):
        self.user_manager = user_manager
        self.message = Message()
        self.context = iter(self.handle_command())
        self.my_id = uid
        self.vk = None
        
    def handle(self, message, vk):
        self.message = message
        self.vk = vk
        return next(self.context)


    def handle_command(self):
        while True:
            if self.message.text == '/почты':
                conn = sqlite3.connect('study.db')
                emails = conn.execute('''select name, email from emails''').fetchall()
                conn.close()

                res_text = '\n'.join(name + ':\n' + email  for name, email in emails)
                answer = Message(text=res_text, keyboard=USER_KEYBOARD)

                answer.send(self.vk, self.my_id)

                yield None

            elif self.message.text == '/ссылки':
                res_text = '\n'.join([
                    "Гугл диск",            "https://drive.google.com/drive/folders/1JnDu4QvpLZbxnZ8w4Spt998eOa0tJ-RE",
                    "СДО",                  "https://dl-iamm.spbstu.ru/",
                    "Личный кабинет",       "lk.spbstu.ru",
                    "Расписание занятий",   "https://ruz.spbstu.ru/faculty/122/groups/30725"
                ])
                answer = Message(text=res_text, keyboard=USER_KEYBOARD)

                answer.send(self.vk, self.my_id)
                yield None

            elif self.message.text == '/задачи':
                tasks = taskmngr.get_user_tasks(self.my_id)
                for task in tasks:
                    task.get_message().send(self.vk, self.my_id)
                    yield None

                    if self.message.text == '/exit':
                        break
                    elif self.message.text != '/next':
                        taskmngr.update_task_answer(task.id, self.my_id, self.message.text[:255])
                        answer = Message(text='Ответ сохранен')
                        answer.send(self.vk, self.my_id)

                answer = Message(text='Выполнение задач завершено', keyboard=USER_KEYBOARD)
                answer.send(self.vk, self.my_id)

                yield None

            elif self.message.text == '/taskinfo':
                task_records = taskmngr.tasks_info()

                for task_text, answers in task_records:
                    res_text = task_text + '\n' + '\n'.join(answers)
                    answer = Message(text=res_text, keyboard=USER_KEYBOARD)
                    answer.send(self.vk, self.my_id)
                
                yield None

            elif self.message.text == '/?':
                res_text = '\n'.join([
                    'Доступные команды:',
                    '/почты',
                    '/ссылки'
                    '/диск',
                    '/расписание',
                    '/задачи',
                    '/taskinfo'
                ])
                answer = Message(text=res_text, keyboard=USER_KEYBOARD)
                answer.send(self.vk, self.my_id)

                yield None

            else:
                self.message.forward(self.vk, self.user_manager.ADMIN)
                yield None



class AdminCommandHandler:
    def __init__(self, uid, user_manager):
        self.user_manager = user_manager
        self.message = Message()
        self.context = iter(self.handle_command())
        self.my_id = uid
        self.vk = None
        
    def handle(self, message, vk):
        self.message = message
        self.vk = vk
        return next(self.context)


    def handle_command(self):
        while True:
            if self.message.text == '/почты':
                conn = sqlite3.connect('study.db')
                emails = conn.execute('''select name, email from emails''').fetchall()
                conn.close()

                res_text = '\n'.join(name + ':\n' + email  for name, email in emails)
                answer = Message(text=res_text, keyboard=USER_KEYBOARD)

                answer.send(self.vk, self.my_id)

                yield None

            elif self.message.text == '/ссылки':
                res_text = '\n'.join([
                    "Гугл диск", "https://drive.google.com/drive/folders/1JnDu4QvpLZbxnZ8w4Spt998eOa0tJ-RE",
                    "СДО", "https://dl-iamm.spbstu.ru/",
                    "Личный кабинет", "lk.spbstu.ru",
                    "Расписание занятий", "https://ruz.spbstu.ru/faculty/122/groups/30725"
                ])
                answer = Message(text=res_text, keyboard=USER_KEYBOARD)

                answer.send(self.vk, self.my_id)
                yield None

            elif self.message.text == '/задачи':
                tasks = taskmngr.get_user_tasks(self.my_id)
                for task in tasks:
                    task.get_message().send(self.vk, self.my_id)
                    yield None

                    if self.message.text == '/exit':
                        break
                    elif self.message.text != '/next':
                        taskmngr.update_task_answer(task.id, self.my_id, self.message.text[:255])
                        answer = Message(text='Ответ сохранен')
                        answer.send(self.vk, self.my_id)

                answer = Message(text='Выполнение задач завершено', keyboard=USER_KEYBOARD)
                answer.send(self.vk, self.my_id)

                yield None

            elif self.message.text == '/taskinfo':
                task_records = taskmngr.tasks_info()

                for task_text, answers in task_records:
                    res_text = task_text + '\n' + '\n'.join(answers)
                    Message(text=res_text, keyboard=USER_KEYBOARD).send(self.vk, self.my_id)
                
                yield None

            elif self.message.text == '/?':
                answer = Message(text='Доступные команды:', keyboard=ADMIN_KEYBOARD)
                answer.send(self.vk, self.my_id)
                yield None

            elif self.message.text == '/forall':
                while True:
                    text='Введите сообщение для всех:'
                    reset_keyboard = VkKeyboard()
                    reset_keyboard.add_button('/reset', VkKeyboardColor.NEGATIVE)
                    answer = Message(text=text, keyboard=reset_keyboard)
                    answer.send(self.vk, self.my_id)
                    yield None

                    if self.message.text == '/reset':
                        answer = Message(text='Сообщение отменено', keyboard=ADMIN_KEYBOARD)
                        answer.send(self.vk, self.my_id)
                        break
                    
                    self.message.keyboard = USER_KEYBOARD
                    result = self.message.send(self.vk, self.user_manager.ids())

                    errors = [status['peer_id'] for status in result if 'error' in status]
                    success = [status['peer_id'] for status in result if 'error' not in status]
                        
                    text = 'Отправлено всем'
                    if errors:
                        text += '\nКроме:\n' + '\n'.join([self.user_manager[uid].name for uid in errors])

                    answer = Message(text=text, keyboard=ADMIN_KEYBOARD)
                    answer.send(self.vk, self.user_manager.ADMIN)

                    break

                yield None

            elif self.message.text == '/forfew':
                while True:
                    text = 'Введите получателей:'
                    reset_keyboard = VkKeyboard()
                    reset_keyboard.add_button('/reset', VkKeyboardColor.NEGATIVE)
                    answer = Message(text=text, keyboard=reset_keyboard)
                    answer.send(self.vk, self.my_id)
                    yield None

                    if self.message.text == '/reset':
                        answer = Message(text='Сообщение отменено', keyboard=ADMIN_KEYBOARD)
                        answer.send(self.vk, self.my_id)
                        break

                    peers = self.user_manager.ids_from_nicknames(self.message.text.split())

                    text = 'Сообщение будет отправлено:\n' + '\n'.join([self.user_manager[peer].name for peer in peers])
                    text += '\nВведите сообщение'
                    reset_keyboard = VkKeyboard()
                    reset_keyboard.add_button('/reset', VkKeyboardColor.NEGATIVE)
                    answer = Message(text=text, keyboard=reset_keyboard)
                    answer.send(self.vk, self.my_id)
                    yield None

                    if self.message.text == '/reset':
                        answer = Message(text='Сообщение отменено', keyboard=ADMIN_KEYBOARD)
                        answer.send(self.vk, self.my_id)
                        break

                    self.message.keyboard = USER_KEYBOARD
                    result = self.message.send(self.vk, peers)

                    errors = [status['peer_id'] for status in result if 'error' in status]
                    success = [status['peer_id'] for status in result if 'error' not in status]
                        
                    text = 'Отправлено:\n' + '\n'.join([self.user_manager[uid].name for uid in success])
                    if errors:
                        text += '\nКроме:\n' + '\n'.join([self.user_manager[uid].name for uid in errors])

                    answer = Message(text=text, keyboard=ADMIN_KEYBOARD)
                    answer.send(self.vk, self.user_manager.ADMIN)

                    break

                yield None

            elif self.message.text == '/newtask':
                asktask = None

                while True:
                    text='Введите задачу:'
                    reset_keyboard = VkKeyboard()
                    reset_keyboard.add_button('/reset', VkKeyboardColor.NEGATIVE)
                    answer = Message(text=text, keyboard=reset_keyboard)
                    answer.send(self.vk, self.my_id)
                    yield None

                    if self.message.text == '/reset':
                        answer = Message(text='Создание задачи отменено', keyboard=ADMIN_KEYBOARD)
                        answer.send(self.vk, self.my_id)
                        break
                    
                    task = Task(self.message.id, self.message)

                    kb = VkKeyboard(one_time=True)
                    kb.add_button('/empty')
                    kb.add_button('/yes_no')
                    kb.add_line()
                    kb.add_button('/reset', VkKeyboardColor.NEGATIVE)

                    answer = Message(text='Введите варианты ответа (по одному на строке):',
                                    keyboard=kb)

                    answer.send(self.vk, self.my_id)
                    yield None

                    
                    if self.message.text == '/reset':
                        answer = Message(text='Создание задачи отменено', keyboard=ADMIN_KEYBOARD)
                        answer.send(self.vk, self.my_id)
                        break

                    if self.message.text == '/empty':
                        pass
                    elif self.message.text == '/yes_no':
                        task.append_answer(Answer('да', VkKeyboardColor.POSITIVE))
                        task.append_answer(Answer('нет', VkKeyboardColor.NEGATIVE))
                    elif self.message.text.startswith('/range'):
                        try:
                            ans_cnt = int(self.message.text[6:])
                            for answer in range(1, ans_cnt + 1):
                                task.append_answer(Answer(str(answer)))
                        except Exception as e:
                            print(e)
                            break

                    else:
                        for answer in self.message.text.split('\n'):
                            task.append_answer(Answer(answer))

                    task.get_preview().send(self.vk, self.my_id)
                    kb = VkKeyboard(one_time=True)
                    kb.add_button('/done', VkKeyboardColor.POSITIVE)
                    kb.add_button('/reset', VkKeyboardColor.NEGATIVE)

                    preview = Message(text='Подтвердите создание',
                                    keyboard=kb)

                    preview.send(self.vk, self.my_id)

                    yield None

                    if self.message.text == '/reset':
                        answer = Message(text='Создание задачи отменено', keyboard=ADMIN_KEYBOARD)
                        answer.send(self.vk, self.my_id)
                        break

                    task.save()

                    answer = Message(text='Задача создана', keyboard=ADMIN_KEYBOARD)

                    answer.send(self.vk, self.my_id)

                    asktask = Message(text='/задачи')
                    break

                yield asktask


            elif self.message.text == '/exitadmin':
                answer = Message(text='Доступные команды:', keyboard=USER_KEYBOARD)
                answer.send(self.vk, self.my_id)
                yield None

            else:
                res_text = '\n'.join([
                    'Доступные команды:',
                    '/почты',
                    '/ссылки'
                    '/диск',
                    '/расписание',
                    '/задачи',
                    '/taskinfo'
                ])
                answer = Message(text=res_text, keyboard=USER_KEYBOARD)
                answer.send(self.vk, self.my_id)

                yield None
