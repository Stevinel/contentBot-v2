import os
import telebot
import datetime as dt
from django.core.management.base import BaseCommand
from bot.models import Channel, Video 

from bot.keyboard_config import get_hello_keyboard, get_actions_keyboard, get_back_keyboard, get_pictures
from time import sleep
from bot.loguru_config import logger
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
BOT = telebot.TeleBot(TELEGRAM_TOKEN)
DATE_FORMAT = "%d.%m.%Y"


@logger.catch
@BOT.message_handler(commands=["start"])
def start_message(message):
    """
    Функция приветствия, выводит сообщение\
    и пару кнопок на выбор для дальнейшних действий
    """
    MARKUP = get_hello_keyboard()
    picture = get_pictures()
    BOT.send_photo(
        message.chat.id,
        photo=picture["HELLO_PHOTO"],
        caption=f"Привет, калтэнтеры!\n"
        f"Сегодня {dt.date.today().strftime(DATE_FORMAT)}\n"
        "Cмотрите описание бота и используйте команды.\n",
        reply_markup=MARKUP
    )


def get_full_menu(call):
    """Функция отображает все кнопки меню"""
    MARKUP = get_actions_keyboard()
    picture = get_pictures()
    BOT.send_photo(
    call.message.chat.id,
    photo=picture["SHREK_THINKING"],
    caption="Чего желаете?",
    reply_markup=MARKUP,
    )

@BOT.callback_query_handler(func=lambda call:True)
def query_handler(call):
    """Функция распределяет дальнейшие действия в зависимости
    от условия полученной команды"""
    picture = get_pictures()
    if call.data == '1': # Продолжить
        get_full_menu(call)
    elif call.data == '2': # Уйти
        BOT.send_animation(call.message.chat.id, animation=picture["BYE"])
        BOT.answer_callback_query(callback_query_id=call.id, text='Пока-пока!')
        BOT.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == '6': # Показать все видео
        show_all_videos(call.message)
    elif call.data == "8": # Вернуться в меню
        get_full_menu(call)


@logger.catch
def show_all_videos(message):
    """Функция показывает все имеющиеся видео в БД"""
    MARKUP = get_back_keyboard()
    urls = Video.objects.all().order_by("-video_rating")

    if urls:
        for url in urls:
            BOT.send_message(message.chat.id, url.url)
        BOT.send_message(
                message.chat.id,
                "Список окончен, можете вернуться назад.",
                reply_markup=MARKUP
        )
        BOT.edit_message_reply_markup(message.chat.id, message.message_id)
    else:
        BOT.send_message(message.chat.id, "Нет видео.", reply_markup=MARKUP)

class Command(BaseCommand):
    help = "Телеграм-бот"

    @BOT.message_handler(func=lambda message: True, content_types=['text'])
    def handle(self, *args, **options):
        sleep(3)
        BOT.polling()
