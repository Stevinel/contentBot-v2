from telebot import types
from dotenv import load_dotenv
load_dotenv()


HELLO_PHOTO = open('images/Приветствие.jpg', 'rb')
SHREK_THINKING = open('images/Шрек думает.jpg', 'rb')
BYE = open('images/Прощание.gif', 'rb')


def get_hello_keyboard():
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text='Продолжить', callback_data=1))
    MARKUP.add(types.InlineKeyboardButton(text='Уйти', callback_data=2))
    return MARKUP

def get_actions_keyboard():
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="🍻 Смотреть контент", callback_data=3))
    MARKUP.add(types.InlineKeyboardButton(text="📀 Добавить видео", callback_data=4))
    MARKUP.add(types.InlineKeyboardButton(text="📹 Добавить канал", callback_data=5))
    MARKUP.add(types.InlineKeyboardButton(text="👀 Показать все видео", callback_data=6))
    MARKUP.add(types.InlineKeyboardButton(text="👀 Показать все каналы", callback_data=7))
    MARKUP.add(types.InlineKeyboardButton(text='🖕 Уйти', callback_data=2))
    return MARKUP
