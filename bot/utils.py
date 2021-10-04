import datetime as dt
import os
from time import sleep

import requests

from bot.api_urls import *
from bot.models import Channel, Video

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
import bot.keyboard_config as keyb
import bot.management.commands.bot as bot
from bot.loguru_config import logger
from contentbot.settings import BOT, TELEGRAM_CHAT_ID


@logger.catch
def add_channel_url(message):
    """Функция ожидает ссылку на канал и переходит к функции
    ввода рейтинга для канала"""
    msg = BOT.send_message(message.chat.id, "~~~Введите ссылку на канал~~~")
    BOT.register_next_step_handler(msg, add_channel_raiting)


@logger.catch
def add_channel_raiting(message):
    """Функция проверяет корректность ссылки на канал, если всё верно,
    то переходит к следующей функции добавления канала"""
    try:
        if message.text.startswith("https://www.youtube.com/") or message.text.startswith(
            "https://youtube.com/"
        ):
            msg = BOT.send_message(
                message.chat.id,
                "~~~Введите рейтинг канала от 1 до 10\n"
                "Видео будут упорядочены по рейтингу канала~~~",
            )
            channel_url = message.text
            BOT.register_next_step_handler(msg, bot.add_channel, channel_url)
        else:
            BOT.send_message(
                message.chat.id,
                "~~~Вы ввели неправильные данные, начните заново~~~",
            )
    except:
        BOT.send_message(message.chat.id, "~~~Произошла ошибка~~~")


@logger.catch
def check_channel_data(message, channel_url):
    """Функция достаёт данные из ссылки, для добавления нового канала"""
    channel_rating = message.text
    if len(channel_url.split("/")):
        cut_link = channel_url.split("/")[4:]
    eng_channel_name = cut_link[0]
    name_lenght = len(eng_channel_name)

    if name_lenght < 24:
        response = requests.get(
            GET_CHANNEL_BY_USERNAME + eng_channel_name + "&key=" + GOOGLE_API_KEY
        )
    else:
        response = requests.get(GET_CHANNEL_BY_ID + eng_channel_name + "&key=" + GOOGLE_API_KEY)
    sleep(1)
    if "items" not in response:
        response = requests.get(SEARCH_BROKEN_CHANNEL + eng_channel_name + "&key=" + GOOGLE_API_KEY)
        channel_name = response.json()["items"][0]["snippet"]["channelTitle"]
    else:
        channel_name = response.json()["items"][0]["snippet"]["title"]
    return channel_name, channel_rating


@logger.catch
def add_url_new_videos(message):
    """Функция ожидаает ссылку с видео и переходит в функции,
    которая добавляет эту ссылку в БД"""
    BOT.send_message(
        message.chat.id,
        "~~~Отправьте ссылку на видео, я добавлю его в базу~~~",
    )
    BOT.register_next_step_handler(message, bot.add_new_video)


@logger.catch
def check_video_data(message):
    """Функция достаёт данные из ссылки, для добавления нового видео"""
    video_url = message.text

    if len(message.text.split("/")):
        if "=" in message.text:
            cut_link = message.text.split("=")
            eng_channel_name = cut_link[1]
        else:
            cut_link = message.text.split("/")[3:]
            eng_channel_name = cut_link[0]
    response = requests.get(GET_CHANNEL_ID_FROM_VIDEO + eng_channel_name + "&key=" + GOOGLE_API_KEY)
    channel_name = response.json()["items"][0]["snippet"]["channelTitle"]
    return channel_name, video_url


@logger.catch
def delete_video(message):
    """Функция удаления видео из базы"""
    video = Video.objects.all().order_by("-video_rating")[0]
    video.delete()
    MARKUP = keyb.get_next_video_keyboard()
    BOT.send_message(message.chat.id, "~~~Видео удалено~~~", reply_markup=MARKUP)


@logger.catch
def deferral_video(message):
    """Функция пропустить видео"""
    video = Video.objects.all().order_by("-video_rating")[0]
    video.video_rating = -1
    video.save()
    MARKUP = keyb.get_next_video_keyboard()
    BOT.send_message(message.chat.id, "~~~Видео отложено~~~", reply_markup=MARKUP)


@logger.catch
def query_delete_channel(message):
    """Функция ожидает название канала для удаления и переходит
    к следующей функции, которая удаляет канал"""
    msg = BOT.send_message(
        message.chat.id,
        "~~~Введите канал для удаления:~~~",
    )
    BOT.register_next_step_handler(msg, bot.delete_channel)


@logger.catch
def check_new_video(url):
    if len(url.split("/")):
        cut_link = url.split("/")[4:]
        eng_channel_name = cut_link[0]
        name_lenght = len(eng_channel_name)
        if name_lenght < 24:
            get_channel_info = requests.get(
                GET_CHANNEL_BY_USERNAME + eng_channel_name + "&key=" + GOOGLE_API_KEY
            )
        else:
            get_channel_info = requests.get(
                GET_CHANNEL_BY_ID + eng_channel_name + "&key=" + GOOGLE_API_KEY
            )
        if "items" not in get_channel_info:
            get_channel_info = requests.get(
                SEARCH_BROKEN_CHANNEL + eng_channel_name + "&key=" + GOOGLE_API_KEY
            )
            channel_name = get_channel_info.json()["items"][0]["snippet"]["channelTitle"]
            channel_id = get_channel_info.json()["items"][0]["snippet"]["channelId"]
        else:
            channel_name = get_channel_info.json()["items"][0]["snippet"]["title"]
            channel_id = get_channel_info.json()["items"][0]["id"]
        search_new_video = requests.get(
            SEARCH_VIDEO_BY_CHANNEL_ID + channel_id + "&maxResults=30&key=" + GOOGLE_API_KEY
        )
        date_of_publication = search_new_video.json()["items"][0]["snippet"]["publishedAt"][:10]
        video_id = search_new_video.json()["items"][0]["id"]
        video_id_in_broken_channels = search_new_video.json()["items"][1]["id"]
        if "videoId" in video_id:
            new_video = YOUTUBE_URL + video_id["videoId"]
        else:
            new_video = YOUTUBE_URL + video_id_in_broken_channels["videoId"]
        date_today = str(dt.date.today())
        if date_of_publication == date_today:
            channels_rating = Channel.objects.filter(title=channel_name).values_list("rating")[0]
            channel_rating = "".join(str(x) for x in channels_rating)
            new_video = Video.objects.create(
                video_channel_name=channel_name,
                url=new_video,
                video_rating=channel_rating,
            )
            BOT.send_message(TELEGRAM_CHAT_ID, f"Добавлено новое видео c канала '{channel_name}'")
            logger.info("Bot added video")
        else:
            logger.info("No new videos were found")
