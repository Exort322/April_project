import requests
import telebot
from telebot import types
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '7970086489:AAG9u_6S0Qz75qujtFOG2I-OeM-7XunvgLA'
url = f'https://api.telegram.org/bot{TOKEN}/deleteWebhook'
response = requests.get(url)
bot = telebot.TeleBot(TOKEN)


class Bot:
    def __init__(self, users_db):
        self.language = None
        self.waiting_for_joke = False
        self.users_db = users_db
        self.texts = {
            'en': {
                'welcome': 'Hello! I am a silly joke bot. I can help you create jokes or tell random jokes.',
                'choose_language': 'Please choose your language:',
                'language_selected': 'Language selected: English',
                'choose_action': 'Choose an action:',
                'joke_added': 'Joke added: {}',
                'enter_joke': 'Please enter your joke:',
                'my_jokes': 'You have not written any jokes yet.',
                'viewed_jokes_history': 'You have not viewed any jokes yet.',
                'buttons': {
                    'profile': 'Profile 👤',
                    'my_jokes': 'Written Jokes 📜',
                    'create_joke': 'Create Joke ✍️',
                    'viewed_jokes': 'Viewed Jokes History 📚',
                    'random_joke': 'Get Random Joke 🎉'
                }
            },
            'ru': {
                'welcome': 'Привет! Я глупый шут. Я могу помочь вам создавать шутки или рассказывать случайные шутки.',
                'choose_language': 'Пожалуйста, выберите язык:',
                'language_selected': 'Язык выбран: Русский',
                'choose_action': 'Выберите действие:',
                'joke_added': 'Шутка добавлена: {}',
                'enter_joke': 'Пожалуйста, введите вашу шутку:',
                'my_jokes': 'Вы еще не написали ни одной шутки.',
                'viewed_jokes_history': 'Вы еще не просмотрели ни одной шутки.',
                'buttons': {
                    'profile': 'Профиль 👤',
                    'my_jokes': 'Написанные шутки 📜',
                    'create_joke': 'Создать шутку ✍️',
                    'viewed_jokes': 'История просмотренных шуток 📚',
                    'random_joke': 'Получить случайную шутку 🎉'
                }
            }
        }

    def start(self, message):
        self.language = None
        self.waiting_for_joke = False
        self.is_processing = False
        bot.send_message(message.chat.id, self.texts['ru']['welcome'])

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("English 🇬🇧"), types.KeyboardButton("Русский 🇷🇺"))

        self.users_db.new_user(message.chat.id, message.from_user.username)
        bot.send_message(message.chat.id, self.texts['ru']['choose_language'], reply_markup=markup)

    def handle_language_selection(self, message):
        if message.text in ['English 🇬🇧', 'Русский 🇷🇺']:
            self.language = 'en' if message.text == 'English 🇬🇧' else 'ru'
            bot.send_message(message.chat.id, self.texts[self.language]['language_selected'])
            self.show_action_buttons(message.chat.id)

    def show_action_buttons(self, chat_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            types.KeyboardButton(self.texts[self.language]['buttons']['profile']),
            types.KeyboardButton(self.texts[self.language]['buttons']['my_jokes']),
            types.KeyboardButton(self.texts[self.language]['buttons']['create_joke']),
            types.KeyboardButton(self.texts[self.language]['buttons']['viewed_jokes']),
            types.KeyboardButton(self.texts[self.language]['buttons']['random_joke'])
        )
        bot.send_message(chat_id, self.texts[self.language]['choose_action'], reply_markup=markup)

    def send_random_joke(self, chat_id):
        # здесь нужно шутки из бд
        pass

    def handle_joke_input(self, message):
        if self.waiting_for_joke:
            joke = message.text
            bot.send_message(message.chat.id, self.texts[self.language]['joke_added'].format(joke))
            self.waiting_for_joke = False
            self.show_action_buttons(message.chat.id)

    def handle_profile(self, chat_id):
        username = None
        written_jokes_count = None
        viewed_jokes_count = None

        profile_info = (
            f"**👤 Профиль пользователя**\n"
            f"**Имя пользователя:** {username}\n"
            f"**🌐 Язык:** {self.language}\n"
            f"**✍️ Количество написанных шуток:** {written_jokes_count}\n"
            f"**📜 Количество просмотренных шуток:** {viewed_jokes_count}\n"
        )

        bot.send_message(chat_id, profile_info, parse_mode='Markdown')

    def handle_written_jokes(self, chat_id):
        written_jokes_count = 0
        if written_jokes_count == 0:
            bot.send_message(chat_id, self.texts[self.language]['my_jokes'])
        else:
            bot.send_message(chat_id, f"You have written {written_jokes_count} jokes.")

    def handle_viewed_jokes(self, chat_id):
        viewed_jokes_count = 0
        if viewed_jokes_count == 0:
            bot.send_message(chat_id, self.texts[self.language]['viewed_jokes_history'])
        else:
            bot.send_message(chat_id, f"You have viewed {viewed_jokes_count} jokes.")

    def run(self):
        @bot.message_handler(commands=['start'])
        def start_handler(message):
            self.start(message)
            self.users_db.activity(message.from_user.id)

        @bot.message_handler(commands=['my_jokes'])
        def my_jokes_handler(message):
            self.handle_written_jokes(message.chat.id)

        @bot.message_handler(commands=['random_joke'])
        def random_jokes_handler(message):
            self.send_random_joke(message)

        @bot.message_handler(commands=['create_joke'])
        def create_joke_handler(message):
            self.waiting_for_joke = True
            bot.send_message(message.chat.id, self.texts[self.language]['enter_joke'])

        @bot.message_handler(commands=['language'])
        def language_handler(message):
            self.handle_language_selection(message)

        @bot.message_handler(commands=['profile'])
        def profile_handler(message):
            self.handle_profile(message.chat.id)

        @bot.message_handler(func=lambda message: True)
        def message_handler(message):
            if self.language is None:
                self.handle_language_selection(message)
            elif message.text == self.texts[self.language]['buttons']['profile']:
                self.handle_profile(message.chat.id)
            elif message.text == self.texts[self.language]['buttons']['my_jokes']:
                self.handle_written_jokes(message.chat.id)
            elif message.text == self.texts[self.language]['buttons']['create_joke']:
                self.waiting_for_joke = True
                bot.send_message(message.chat.id, self.texts[self.language]['enter_joke'])
            elif message.text == self.texts[self.language]['buttons']['viewed_jokes']:
                self.handle_viewed_jokes(message.chat.id)
            else:
                self.handle_joke_input(message)

            self.users_db.activity(message.from_user.id)
        bot.polling(none_stop=True)
