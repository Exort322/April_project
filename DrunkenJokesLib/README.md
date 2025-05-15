# JokeLib 🃏

Python библиотека для работы с шутками: интеграция с внешними API, управление историей просмотров и рейтингами. Идеально для чат-ботов и веб-приложений!

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Основные возможности

- 🏆 **Шутка дня** (по рейтингу пользователей)
- 🖼️ **Шутки с картинками**
- 📂 **Категории шуток** (Programming, Dark, Spooky и др.)
- 📝 **Добавление пользовательских шуток**
- ⏳ **История просмотренных шуток**
- ⭐ **Система оценок** (1-5 звёзд)

## Установка

```bash
pip install jokelib
```

## Требования:

Python 3.9+

Зависимости: requests >= 2.25.1, 
python-dateutil>=2.8.2

## Быстрый старт:

```bash
from jokelib import JokeLibrary

# Инициализация библиотеки
lib = JokeLibrary()

# Получить шутку дня
joke_of_day = lib.get_joke_of_the_day()
print(f"Шутка дня: {joke_of_day.text}")

# Получить шутку с картинкой
joke_with_image = lib.get_joke_with_image('Programming')
print(f"{joke_with_image.text}\nImage URL: {joke_with_image.image_url}")

# Добавить свою шутку
new_joke = lib.add_user_joke(
    "колобок повесился, лол"
)
print(f"Добавлена шутка ID: {new_joke.id}")

# Оценить шутку
lib.rate_joke('123abc', 5)
```

## Структура библиотеки:

``` bash
jokelib/
├── __init__.py      # Основной интерфейс библиотеки
├── database.py      # Работа с SQLite базой
├── api_client.py    # Клиенты для JokeAPI и Unsplash
├── models.py        # Дата-классы для шуток
└── exceptions.py    # Пользовательские исключения
```
## Основные методы:
  
**get_joke_of_the_day()** - 	Лучшая шутка по оценкам

**get_joke_with_image(category)** - 	Шутка с рандомной картинкой

**add_user_joke(text, category** -	Добавить свою шутку

**rate_joke(joke_id, rating)**	 - Оценить шутку (1-5)

**get_categories()** - 	Список доступных категорий
