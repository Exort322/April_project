from DrunkenJokesLib import *
# Инициализация библиотеки
lib = JokeLibrary()

# Шутка дня
print("Шутка дня:", lib.get_joke_of_the_day().text)

joke = lib.get_joke_with_image('Programming', 'programming,hacker')
print(f"{joke.text}\nImage: {joke.image_url}")

new_joke = lib.add_user_joke(
    "Почему программисты путают Хэллоуин и Рождество? "
    "Потому что Oct 31 == Dec 25!"
)
print(f"Добавлена шутка ID: {new_joke.id}")