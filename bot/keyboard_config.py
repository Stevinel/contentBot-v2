from telebot import types
from dotenv import load_dotenv
load_dotenv()


def get_pictures():
    """Функция возвращает картинки для отправки пользователю"""
    pictures = {
    'HELLO_PHOTO': open('bot/management/commands/images/Приветствие.jpg', 'rb'),
    'SHREK_THINKING': open('bot/management/commands/images/Шрек думает.jpg', 'rb'),
    'BYE': open('bot/management/commands/images/Прощание.gif', 'rb')
    }
    return pictures


def get_hello_keyboard():
    """Клавиатура приветствия"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text='🐾 Продолжить', callback_data=1))
    MARKUP.add(types.InlineKeyboardButton(text='🖕 Уйти', callback_data=2))
    return MARKUP


def get_actions_keyboard():
    """Клавиатура меню"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="🍻 Смотреть контент", callback_data=3))
    MARKUP.add(types.InlineKeyboardButton(text="📀 Добавить видео", callback_data=4))
    MARKUP.add(types.InlineKeyboardButton(text="📹 Добавить канал", callback_data=5))
    MARKUP.add(types.InlineKeyboardButton(text="👀 Показать все видео", callback_data=6))
    MARKUP.add(types.InlineKeyboardButton(text="👀 Показать все каналы", callback_data=7))
    MARKUP.add(types.InlineKeyboardButton(text='🖕 Уйти', callback_data=2))
    return MARKUP

def get_back_keyboard():
    """Клавиатура возврата в меню"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="👈 Вернуться в меню", callback_data=8))
    return MARKUP
    