import sqlite3
import datetime


class Users_db:
    def __init__(self):
        con = sqlite3.connect("back/users.db")
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users_info ('
                    'id INT,'
                    'nickname TEXT,'
                    'messages INT,'
                    'first_activity DATE,'
                    'last_activity DATE)'
                    '')
        con.commit()

    def connection(self):
        con = sqlite3.connect("back/users.db")
        cur = con.cursor()
        return con, cur

    def new_user(self, user_id, nick):
        con, cur = self.connection()
        date = datetime.datetime.now()
        cur.execute('SELECT 1 FROM users_info WHERE id = ?', (int(user_id),))
        if not cur.fetchone():  # чтобы были только уникальные пользователи
            cur.execute(
                'INSERT INTO users_info (id, nickname, messages, first_activity, last_activity) VALUES (?, ?, ?, ?, ?)',
                (int(user_id), nick, 1, date, date)
            )
        con.commit()

    def activity(self, user_id):
        con, cur = self.connection()
        date = datetime.datetime.now()
        cur.execute(f'UPDATE users_info SET last_activity = ?, messages = messages + 1 WHERE id = ?', (date, user_id))
        con.commit()
