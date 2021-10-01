from dotenv import load_dotenv
from telebot import types

load_dotenv()


def get_pictures():
    """Функция возвращает картинки для отправки пользователю"""
    pictures = {
        "HELLO_PHOTO": open("bot/management/commands/images/Приветствие.jpg", "rb"),
        "SHREK_THINKING": open("bot/management/commands/images/Шрек думает.jpg", "rb"),
        "BYE": open("bot/management/commands/images/Прощание.gif", "rb"),
        "ERIC_THINKING": open("bot/management/commands/images/Думаю.jpg", "rb"),
        "CHILL": open("bot/management/commands/images/чил.jpg", "rb"),
        "WHAT": open("bot/management/commands/images/чего.gif", "rb"),
    }
    return pictures


def get_hello_keyboard():
    """Клавиатура приветствия"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="🐾 Продолжить", callback_data=1))
    MARKUP.add(types.InlineKeyboardButton(text="🖕 Уйти", callback_data=2))
    return MARKUP


def get_actions_keyboard():
    """Клавиатура меню"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="🍻 Смотреть контент", callback_data=3))
    MARKUP.add(types.InlineKeyboardButton(text="📀 Добавить видео", callback_data=4))
    MARKUP.add(types.InlineKeyboardButton(text="📹 Добавить канал", callback_data=5))
    MARKUP.add(types.InlineKeyboardButton(text="❌ Удалить канал", callback_data=6))
    MARKUP.add(types.InlineKeyboardButton(text="👀 Показать все видео", callback_data=7))
    MARKUP.add(types.InlineKeyboardButton(text="👀 Показать все каналы", callback_data=8))
    MARKUP.add(types.InlineKeyboardButton(text="🖕 Уйти", callback_data=2))
    return MARKUP


def get_back_keyboard():
    """Клавиатура возврата в меню"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="👈 Вернуться в меню", callback_data=9))
    return MARKUP


def get_show_channels_keyboard():
    """Клавиатура меню при показе всех каналов"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="📹 Добавить канал", callback_data=5))
    MARKUP.add(types.InlineKeyboardButton(text="❌ Удалить канал", callback_data=6))
    MARKUP.add(types.InlineKeyboardButton(text="👈 Вернуться в меню", callback_data=9))
    return MARKUP


def get_show_content_keyboard():
    """Клавиатура меню при показе всех видео"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="👉 Отложить видео", callback_data=11))
    MARKUP.add(types.InlineKeyboardButton(text="❌ Удалить видео", callback_data=12))
    MARKUP.add(types.InlineKeyboardButton(text="👈 Вернуться в меню", callback_data=9))
    return MARKUP


def get_next_video_keyboard():
    """Клавиатура переключения видео"""
    MARKUP = types.InlineKeyboardMarkup()
    MARKUP.add(types.InlineKeyboardButton(text="👉 Следующее видео", callback_data=10))
    return MARKUP
