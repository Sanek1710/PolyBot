import sqlite3

from fuzzywuzzy import fuzz

import command


class UserRole:
    ADMIN = 'admin'
    SUBADMIN = 'submarin'
    USER = 'user'
    TESTER = 'tester'

class User:
    def __init__(self, id, var, name, role, nicknames, user_manager):
        self.id = id
        self.var = var
        self.name = name
        self.role = role
        self.nicknames = nicknames
        if self.role == UserRole.ADMIN:
            self.cmdhandler = command.AdminCommandHandler(id, user_manager)
        else:
            self.cmdhandler = command.CommandHandler(id, user_manager)

    def nickname_match(self, nickname):
        return fuzz.partial_ratio(nickname, self.nicknames)

    def __str__(self):
        return '\n'.join([
            str(self.id),
            str(self.var),
            str(self.name),
            str(self.role),
            str(self.nicknames)
        ])

    def __repr__(self):
        return str(self)

    def is_admin(self):
        return self.role == UserRole.ADMIN


class UserManager:
    def __init__(self):
        conn = sqlite3.connect('study.db')
        students = conn.execute('''select * from students''').fetchall()
        conn.close()
        self.users = { }
        self.ADMIN = None
        self.user_ids = []
        for uid, var, name, role, nicknames in students:
            self.users[uid] = User(uid, var, name, role, nicknames, self)
            if role == UserRole.ADMIN:
                self.ADMIN = uid
            else:
                self.user_ids.append(uid)

    def __getitem__(self, uid) -> User:
        return self.users.get(uid, User(uid, 0, str(uid), 'unk', '', self))

    def ids(self, include_admin = False):
        if include_admin:
            return self.user_ids + [self.ADMIN]
        else:
            return self.user_ids

    def most_possible_user(self, nickname : str):
        nickname = nickname.lower().replace('ё', 'е')
        max_prob = 0
        max_prob_id = None
        for user in self.users.values():
            ref_prob = user.nickname_match(nickname)
            if ref_prob > max_prob:
                max_prob, max_prob_id = ref_prob, user.id
        if max_prob < 50:
            return None
        return max_prob_id

    def ids_from_nicknames(self, nicknames):
        names = []
        for nickname in nicknames:
            name = self.most_possible_user(nickname)
            if name:
                names.append(name)
        return list(set(names))

