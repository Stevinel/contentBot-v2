from django.shortcuts import render
import os
import telebot
import datetime as dt
from loguru_config import logger
from dotenv import load_dotenv
load_dotenv()
from keyboard_config import get_hello_keyboard, HELLO_PHOTO, SHREK_THINKING, get_actions_keyboard, BYE
from time import sleep

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
    BOT.send_photo(
        message.chat.id,
        photo=HELLO_PHOTO,
        caption=f"Привет, калтэнтеры!\n"
        f"Сегодня {dt.date.today().strftime(DATE_FORMAT)}\n"
        "Cмотрите описание бота и используйте команды.\n",
        reply_markup=MARKUP
    )


@BOT.callback_query_handler(func=lambda call:True)
def query_handler(call):
    if call.data == '1':
        MARKUP = get_actions_keyboard()
        BOT.send_photo(
        call.message.chat.id,
        photo=SHREK_THINKING,
        caption="Чего желаете?",
        reply_markup=MARKUP,
    )

    elif call.data == '2':
        BOT.send_animation(call.message.chat.id, animation=BYE)
        BOT.answer_callback_query(callback_query_id=call.id, text='Пока-пока!')
        BOT.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


if __name__ == '__main__':
    BOT.polling()