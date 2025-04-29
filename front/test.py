import telebot
from telebot import types
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '7948726169:AAEuBR4VldQJ-D9WbSAFhlGcp59Ya348624'

bot = telebot.TeleBot(TOKEN)


class Front:
    def __init__(self, users_db):
        self.language = None
        self.waiting_for_joke = False
        self.is_processing = False
        self.users_db = users_db
        self.texts = {
            'en': {
                'welcome': 'Hello! I am a silly joke bot. I can help you create jokes or tell random jokes.',
                'choose_language': 'Please choose your language:',
                'language_selected': 'Language selected: English',
                'choose_action': 'Choose an action:',
                'joke_added': 'Joke added: {}',
                'enter_joke': 'Please enter your joke:',
                'processing': 'Please wait, your previous request is still being processed...'
            },
            'ru': {
                'welcome': 'Привет! Я глупый шут. Я могу помочь вам создавать шутки или рассказывать случайные шутки.',
                'choose_language': 'Пожалуйста, выберите язык:',
                'language_selected': 'Язык выбран: Русский',
                'choose_action': 'Выберите действие:',
                'joke_added': 'Шутка добавлена: {}',
                'enter_joke': 'Пожалуйста, введите вашу шутку:',
                'processing': 'Пожалуйста, подождите, ваш предыдущий запрос все еще обрабатывается...'
            }
        }

    def start(self, message):
        self.language = None
        self.waiting_for_joke = False
        self.is_processing = False
        bot.send_message(message.chat.id, self.texts['ru']['welcome'])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("English", callback_data='en'))
        markup.add(types.InlineKeyboardButton("Русский", callback_data='ru'))
        self.users_db.new_user(message.chat.id, message.from_user.username)
        bot.send_message(message.chat.id, self.texts['ru']['choose_language'], reply_markup=markup)

    def button(self, call):
        if self.is_processing:
            bot.answer_callback_query(call.id, self.texts[self.language]['processing'])
            return

        self.is_processing = True
        if call.data in ['en', 'ru']:
            self.language = call.data
            bot.edit_message_text(text=self.texts[self.language]['language_selected'], chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
            self.show_action_buttons(call.message.chat.id)
        elif call.data == 'create_joke':
            self.waiting_for_joke = True
            bot.send_message(call.message.chat.id, self.texts[self.language]['enter_joke'])

        self.is_processing = False

    def handle_joke_input(self, message):
        if self.waiting_for_joke:
            joke = message.text
            bot.send_message(message.chat.id, self.texts[self.language]['joke_added'].format(joke))
            self.waiting_for_joke = False
            self.show_action_buttons(message.chat.id)

    def show_action_buttons(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Random Joke', callback_data='random_joke'))
        markup.add(types.InlineKeyboardButton('Create Joke', callback_data='create_joke'))
        bot.send_message(chat_id, self.texts[self.language]['choose_action'], reply_markup=markup)

    def run(self):
        @bot.message_handler(commands=['start'])
        def start_handler(message):
            self.start(message)
            self.users_db.activity(message.from_user.id)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.button(call)
            self.users_db.activity(call.from_user.id)

        @bot.message_handler(func=lambda message: True)
        def joke_input_handler(message):
            self.handle_joke_input(message)
            self.users_db.activity(message.from_user.id)

        bot.polling(none_stop=True)