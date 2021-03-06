import sqlite3

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_message import Message


class TaskVisibility:
    CLOSED = 0
    PRIVATE = 1
    PUBLIC = 2

class Answer:
    def __init__(self, value, color:VkKeyboardColor = VkKeyboardColor.SECONDARY):
        self.value = value
        self.color = color
        pass

class Task:
    def __init__(self, id, task_message:Message, answers:list=[]):
        self.id = id
        self.message = task_message
        self.answers = answers
        pass

    def append_answer(self, answer):
        self.answers.append(answer)

    def get_keyboard(self, inline=False):
        kb = VkKeyboard(one_time= not inline, inline = inline)
        if self.answers:
            if len(self.answers) <= 4:
                max_items_in_line = 2
            elif len(self.answers) <= 9:
                max_items_in_line = 3
            elif len(self.answers) <= 16:
                max_items_in_line = 4
            elif len(self.answers) <= 25:
                max_items_in_line = 5
            else:
                self.answers = self.answers[0:25]
                max_items_in_line = 5

            for answer in self.answers:
                if len(kb.lines[-1]) == max_items_in_line:
                    kb.add_line()
                kb.add_button(answer.value, color=answer.color)

            kb.add_line()
        kb.add_button('/exit', color=VkKeyboardColor.PRIMARY)
        kb.add_button('/next', color=VkKeyboardColor.PRIMARY)
        return kb
    
    def get_message(self):
        self.message.keyboard = self.get_keyboard()
        return self.message

    def get_preview(self):
        self.message.keyboard = self.get_keyboard(inline=True)
        return self.message

    def save(self):
        create_task(self.id, self.message.text, ','.join(self.message.attachments), 
            TaskVisibility.PUBLIC, self.answers)
        

def tasks_info():
    conn = sqlite3.connect('study.db')

    tasks = conn.execute('''
    select id, text from tasks
    ''').fetchall()

    tasks_records = []

    for task_id, task_text in tasks:
        data = conn.execute('''
        select students.var
            , students.name
            , students_tasks.answer
        from students_tasks 
            join students 
                on student_id = students.id
        where students_tasks.task_id = (?)
        order by students.var
        ''', (task_id,)).fetchall()

        tasks_records.append((task_text,
            ['%d) %s : %s'%(var, name, val if val else '') for var, name, val in data]
        ))

    conn.close()

    return tasks_records

def get_user_tasks(user_id):
    conn = sqlite3.connect('study.db')
    task_info = conn.execute('''
    select tasks.id, tasks.text, tasks.attachments, tasks.visibility from tasks
    join students_tasks on students_tasks.task_id = tasks.id and students_tasks.student_id = (?)
    where students_tasks.answer is NULL
    ''', (user_id,)).fetchall()

    tasks = []
    for task_id, text, attachments, visibility in task_info:
        data = conn.execute('''
        select students.var
            , students.name
            , students_tasks.answer
        from students_tasks 
            join students 
                on student_id = students.id
        where students_tasks.task_id = (?)
        order by students.var
        ''', (task_id,)).fetchall()

        text += '\n' + '\n'.join(['%d) %s : %s'%(var, name, val if val else '') for var, name, val in data])

        message = Message(text=text, attachments=attachments.split(','))
        
        answers = conn.execute('''
        select val
            , color
        from task_answers
        where task_id = (?)
        order by id
        ''', (task_id, )).fetchall()

        tasks.append(Task(task_id, message, [Answer(*ans) for ans in answers]))

    return tasks


def create_task(task_id, text, attachments : str, visibility : int, answers=[]):
    conn = sqlite3.connect('study.db')
    conn.execute('''
    insert into tasks(id, text, attachments, visibility) 
    values (?, ?, ?, ?)
    ''', (task_id, text, attachments, visibility))
    conn.commit()

    conn.execute('''
    insert into students_tasks(task_id, student_id, answer)
    select (?), id, NULL from students
    ''', (task_id,))

    for id, answer in enumerate(answers):
        conn.execute('''
        insert into task_answers(task_id, id, val, color)
        values (?, ?, ?, ?)
        ''', (task_id, id, answer.value, answer.color.value))

    conn.commit()
    conn.close()

def update_task_answer(task_id, user_id, answer):
    conn = sqlite3.connect('study.db')


    conn.execute('''
    update students_tasks
    set answer = (?)
    where task_id = (?)
        and student_id = (?)
    ''', (answer, task_id, user_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('study.db')
    conn.execute('''delete from tasks where id = (?)''', (task_id,))
    conn.execute('''delete from students_tasks where task_id = (?)''', (task_id,))
    conn.execute('''delete from task_answers where task_id = (?)''', (task_id,))
    conn.commit()
    conn.close()


