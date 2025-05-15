import sqlite3
from typing import Optional, Tuple, List

class DatabaseManager:
    def __init__(self, db_name: str = 'jokes.db'):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Таблица пользовательских шуток
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_jokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    category TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Таблица истории просмотров и оценок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS joke_history (
                    joke_id TEXT NOT NULL,
                    joke_text TEXT NOT NULL,
                    rating INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def add_user_joke(self, text: str, category: str) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_jokes (text, category)
                VALUES (?, ?)
            ''', (text, category))
            conn.commit()
            return cursor.lastrowid

    def get_joke_of_the_day(self) -> Optional[Tuple]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT joke_text, AVG(rating) as avg_rating 
                FROM joke_history 
                GROUP BY joke_id 
                ORDER BY avg_rating DESC 
                LIMIT 1
            ''')
            return cursor.fetchone()

    def add_to_history(self, joke_id: str, joke_text: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO joke_history (joke_id, joke_text)
                VALUES (?, ?)
            ''', (joke_id, joke_text))
            conn.commit()

    def rate_joke(self, joke_id: str, rating: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE joke_history 
                SET rating = ?
                WHERE joke_id = ?
            ''', (rating, joke_id))
            conn.commit()

    def get_history(self, limit: int = 10) -> List[Tuple]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM joke_history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()