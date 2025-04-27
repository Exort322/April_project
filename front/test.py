from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '7948726169:AAEuBR4VldQJ-D9WbSAFhlGcp59Ya348624'


class Front:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self._add_handlers()
        self.language = None
        self.waiting_for_joke = False
        self.texts = {
            'en': {
                'choose_language': 'Please choose your language:',
                'language_selected': 'Language selected: English',
                'choose_action': 'Choose an action:',
                'feature_unavailable': 'This feature is not available yet.',
                'random_joke': 'Random Joke',
                'create_joke': 'Create Joke',
                'joke_added': 'Joke added: {}',
                'enter_joke': 'Please enter your joke:'
            },
            'ru': {
                'choose_language': 'Пожалуйста, выберите язык:',
                'language_selected': 'Язык выбран: Русский',
                'choose_action': 'Выберите действие:',
                'feature_unavailable': 'Эта функция пока недоступна.',
                'random_joke': 'Случайная шутка',
                'create_joke': 'Создать шутку',
                'joke_added': 'Шутка добавлена: {}',
                'enter_joke': 'Пожалуйста, введите вашу шутку:'
            }
        }

    def _add_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.button))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_joke_input))

    async def start(self, update: Update, context) -> None:
        self.language = None
        self.waiting_for_joke = False
        keyboard = [
            [InlineKeyboardButton("English", callback_data='en')],
            [InlineKeyboardButton("Русский", callback_data='ru')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(self.texts['en']['choose_language'], reply_markup=reply_markup)

    async def button(self, update: Update, context) -> None:
        query = update.callback_query
        await query.answer()

        if query.data in ['en', 'ru']:
            self.language = query.data
            await query.edit_message_text(text=self.texts[self.language]['language_selected'])
            await self.show_action_buttons(query.message.chat.id)

        elif query.data == 'create_joke':
            self.waiting_for_joke = True
            await query.message.reply_text(self.texts[self.language]['enter_joke'])

    async def handle_joke_input(self, update: Update, context) -> None:
        if self.waiting_for_joke:
            joke = update.message.text
            await update.message.reply_text(self.texts[self.language]['joke_added'].format(joke))
            self.waiting_for_joke = False
            await self.show_action_buttons(update.message.chat.id)

    async def show_action_buttons(self, chat_id: int) -> None:
        keyboard = [
            [InlineKeyboardButton(self.texts[self.language]['random_joke'], callback_data='random_joke')],
            [InlineKeyboardButton(self.texts[self.language]['create_joke'], callback_data='create_joke')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.application.bot.send_message(chat_id, self.texts[self.language]['choose_action'], reply_markup=reply_markup)

    def run(self):
        self.application.run_polling()
