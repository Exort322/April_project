import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

DATABASE_NAME = 'jokes.db'
print(1)


def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        registration_date DATETIME NOT NULL,
        last_activity DATETIME NOT NULL
    )
    ''')

    # Таблица шуток
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jokes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        category TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        likes INTEGER DEFAULT 0,
        dislikes INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Таблица оценок пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_ratings (
        user_id INTEGER NOT NULL,
        joke_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,  -- 1 for like, -1 for dislike
        PRIMARY KEY (user_id, joke_id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (joke_id) REFERENCES jokes (id)
    )
    ''')

    conn.commit()
    conn.close()


def add_user(username: str, email: str, password_hash: str) -> int:
    """Добавление нового пользователя"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, registration_date, last_activity)
        VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, datetime.now(), datetime.now()))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return -1  # Пользователь с таким именем или email уже существует
    finally:
        conn.close()


def get_user_by_username(username: str) -> Optional[Dict]:
    """Получение пользователя по имени"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password_hash': user[3],
            'registration_date': user[4],
            'last_activity': user[5]
        }
    return None


def update_user_activity(user_id: int):
    """Обновление времени последней активности пользователя"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE users SET last_activity = ? WHERE id = ?
    ''', (datetime.now(), user_id))

    conn.commit()
    conn.close()


def add_joke(user_id: int, text: str, category: str) -> int:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO jokes (user_id, text, category, created_at)
    VALUES (?, ?, ?, ?)
    ''', (user_id, text, category, datetime.now()))

    joke_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return joke_id


def get_joke(joke_id: int) -> Optional[Dict]:
    """Получение шутки по ID"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT j.*, u.username 
    FROM jokes j
    JOIN users u ON j.user_id = u.id
    WHERE j.id = ?
    ''', (joke_id,))

    joke = cursor.fetchone()
    conn.close()

    if joke:
        return {
            'id': joke[0],
            'user_id': joke[1],
            'text': joke[2],
            'category': joke[3],
            'created_at': joke[4],
            'likes': joke[5],
            'dislikes': joke[6],
            'username': joke[7]
        }
    return None


def get_random_joke(user_id: Optional[int] = None) -> Optional[Dict]:
    """Получение случайной шутки"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Если указан user_id, исключаем шутки, которые пользователь уже оценивал
    if user_id:
        cursor.execute('''
        SELECT j.*, u.username 
        FROM jokes j
        JOIN users u ON j.user_id = u.id
        WHERE j.id NOT IN (
            SELECT joke_id FROM user_ratings WHERE user_id = ?
        )
        ORDER BY RANDOM() LIMIT 1
        ''', (user_id,))
    else:
        cursor.execute('''
        SELECT j.*, u.username 
        FROM jokes j
        JOIN users u ON j.user_id = u.id
        ORDER BY RANDOM() LIMIT 1
        ''')

    joke = cursor.fetchone()
    conn.close()

    if joke:
        return {
            'id': joke[0],
            'user_id': joke[1],
            'text': joke[2],
            'category': joke[3],
            'created_at': joke[4],
            'likes': joke[5],
            'dislikes': joke[6],
            'username': joke[7]
        }
    return None


def rate_joke(user_id: int, joke_id: int, rating: int) -> bool:
    """Оценка шутки пользователем (1 - лайк, -1 - дизлайк)"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        # Проверка не оценивал ли пользователь эту шутку ранее
        cursor.execute('SELECT rating FROM user_ratings WHERE user_id = ? AND joke_id = ?', (user_id, joke_id))
        existing_rating = cursor.fetchone()

        if existing_rating:
            # Если оценка такая же
            if existing_rating[0] == rating:
                return False

            # Удаляю предыдущую оценку и обновляем счетчики
            cursor.execute('DELETE FROM user_ratings WHERE user_id = ? AND joke_id = ?', (user_id, joke_id))
            if existing_rating[0] == 1:
                cursor.execute('UPDATE jokes SET likes = likes - 1 WHERE id = ?', (joke_id,))
            else:
                cursor.execute('UPDATE jokes SET dislikes = dislikes - 1 WHERE id = ?', (joke_id,))

        # Добавляю новую оценку
        cursor.execute('INSERT INTO user_ratings (user_id, joke_id, rating) VALUES (?, ?, ?)',
                       (user_id, joke_id, rating))

        # Обновляю счетчики лайков/дизлайков
        if rating == 1:
            cursor.execute('UPDATE jokes SET likes = likes + 1 WHERE id = ?', (joke_id,))
        else:
            cursor.execute('UPDATE jokes SET dislikes = dislikes + 1 WHERE id = ?', (joke_id,))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


def get_popular_jokes(limit: int = 5) -> List[Dict]:
    """Получение популярных шуток (по количеству лайков)"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT j.*, u.username 
    FROM jokes j
    JOIN users u ON j.user_id = u.id
    ORDER BY j.likes DESC, j.dislikes ASC
    LIMIT ?
    ''', (limit,))

    jokes = []
    for joke in cursor.fetchall():
        jokes.append({
            'id': joke[0],
            'user_id': joke[1],
            'text': joke[2],
            'category': joke[3],
            'created_at': joke[4],
            'likes': joke[5],
            'dislikes': joke[6],
            'username': joke[7]
        })

    conn.close()
    return jokes


def get_user_jokes(user_id: int) -> List[Dict]:
    """Получение всех шуток пользователя"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM jokes WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,))

    jokes = []
    for joke in cursor.fetchall():
        jokes.append({
            'id': joke[0],
            'user_id': joke[1],
            'text': joke[2],
            'category': joke[3],
            'created_at': joke[4],
            'likes': joke[5],
            'dislikes': joke[6]
        })

    conn.close()
    return jokes


def get_user_jokes_count(user_id: int) -> int:
    """Получение количества шуток пользователя"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM jokes WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


# Инициализация базы данных при первом импорте
init_db()