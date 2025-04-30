from bot import Bot
from back.users_db import Users_db


if __name__ == '__main__':
    users_database = Users_db()
    front = Bot(users_database)
    front.run()

