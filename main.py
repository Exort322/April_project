from front.test import Front
from back.users_db import Users_db


if __name__ == '__main__':
    users_database = Users_db()
    front = Front(users_database)
    front.run()
