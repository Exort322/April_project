class JokeAPIError(Exception):
    """Ошибка при работе с API шуток"""

class ImageAPIError(Exception):
    """Ошибка при получении изображения"""

class DatabaseError(Exception):
    """Ошибка работы с базой данных"""