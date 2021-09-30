import requests
from bot.api_urls import *
import os
from time import sleep
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
from bot.loguru_config import logger
import bot.management.commands.bot as bot
from contentbot.settings import BOT

@logger.catch
def add_channel_url(message):
    """Функция ожидает ссылку на канал и переходит к функции
    ввода рейтинга для канала"""
    msg = BOT.send_message(message.chat.id, "Введите ссылку на канал.")
    BOT.register_next_step_handler(msg, add_channel_raiting)


@logger.catch
def add_channel_raiting(message):
    """Функция проверяет корректность ссылки на канал, если всё верно,
    то переходит к следующей функции добавления канала"""
    try:
        if message.text.startswith(
            "https://www.youtube.com/"
        ) or message.text.startswith("https://youtube.com/"):
            msg = BOT.send_message(
                message.chat.id,
                "~~Введите рейтинг канала от 1 до 10\n"
                "Видео будут упорядочены по рейтингу канала.~~",
            )
            channel_url = message.text
            BOT.register_next_step_handler(msg, bot.add_channel, channel_url)
        else:
            BOT.send_message(
                message.chat.id, "~~Вы ввели неправильные данные, начните заново.~~"
            )
    except:
        BOT.send_message(message.chat.id, "~~Произошла ошибка.~~")


@logger.catch
def check_channel_data(message, channel_url):
    channel_rating = message.text
    if len(channel_url.split("/")):
        cut_link = channel_url.split("/")[4:]
    eng_channel_name = cut_link[0]
    name_lenght = len(eng_channel_name)

    if name_lenght < 24:
        response = requests.get(
            GET_CHANNEL_BY_USERNAME
            + eng_channel_name
            + "&key="
            + GOOGLE_API_KEY
        )
    else:
        response = requests.get(
            GET_CHANNEL_BY_ID
            + eng_channel_name
            + "&key="
            + GOOGLE_API_KEY
        )
    sleep(1)
    if "items" not in response:
        response = requests.get(
            SEARCH_BROKEN_CHANNEL
            + eng_channel_name
            + "&key="
            + GOOGLE_API_KEY
        )
        channel_name = response.json()["items"][0]["snippet"][
            "channelTitle"
        ]
    else:
        channel_name = response.json()["items"][0]["snippet"]["title"]
    return channel_name, channel_rating


@logger.catch
def add_url_new_videos(message):
    """Функция ожидаает ссылку с видео и переходит в функции,
    которая добавляет эту ссылку в БД"""
    BOT.send_message(
        message.chat.id, "~~Отправьте ссылку на видео, я добавлю его в базу.~~"
    )
    BOT.register_next_step_handler(message, bot.add_new_video)


@logger.catch
def check_video_data(message):
    video_url = message.text

    if len(message.text.split("/")):
        if "=" in message.text:
            cut_link = message.text.split("=")
            eng_channel_name = cut_link[1]
        else:
            cut_link = message.text.split("/")[3:]
            eng_channel_name = cut_link[0]
    response = requests.get(
        GET_CHANNEL_ID_FROM_VIDEO
        + eng_channel_name
        + "&key="
        + GOOGLE_API_KEY
    )
    channel_name = response.json()["items"][0]["snippet"]["channelTitle"]
    return channel_name, video_url


@logger.catch
def query_delete_channel(message):
    """Функция ожидает название канала для удаления и переходит
    к следующей функции, которая удаляет канал"""
    msg = BOT.send_message(
        message.chat.id,
        "~~Введите канал для удаления:~~",
    )
    BOT.register_next_step_handler(msg, bot.delete_channel)