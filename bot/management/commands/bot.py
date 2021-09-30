import os
import telebot
import datetime as dt
from django.core.management.base import BaseCommand
from bot.models import Channel, Video 

from bot.keyboard_config import *
from time import sleep
from bot.loguru_config import logger
from dotenv import load_dotenv
load_dotenv()
import threading
from bot.utils import check_channel_data, add_channel_url, query_delete_channel, check_video_data, add_url_new_videos

from contentbot.settings import BOT, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


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


@BOT.message_handler(commands=["menu"])
def get_full_menu(message):
    """Функция отображает все кнопки меню"""
    MARKUP = get_actions_keyboard()
    picture = get_pictures()
    BOT.send_photo(
    message.chat.id,
    photo=picture["SHREK_THINKING"],
    caption="Чего желаете?",
    reply_markup=MARKUP,
    )


@BOT.callback_query_handler(func=lambda call:True)
def query_handler(call):
    """Функция распределяет дальнейшие действия в зависимости
    от условия полученной команды"""
    MARKUP = get_back_keyboard()
    picture = get_pictures()

    if call.data == '1': # Продолжить
        get_full_menu(call.message)
    elif call.data == '2': # Уйти
        BOT.send_animation(call.message.chat.id, animation=picture["BYE"], reply_markup=MARKUP)
        BOT.answer_callback_query(callback_query_id=call.id, text='~~Пока-пока!~~')
        # BOT.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == '4': # Добавить видео
        add_url_new_videos(call.message)
    elif call.data == '5': # Добавить канал
        add_channel_url(call.message)
    elif call.data == "6": # Удалить канал
        query_delete_channel(call.message)
    elif call.data == '7': # Показать все видео
        show_all_videos(call.message)
    elif call.data == '8': # Показать все каналы
        show_all_channels(call.message)
    elif call.data == "9": # Вернуться в меню
        get_full_menu(call.message)


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
                "~~Список окончен, можете вернуться назад.~~",
                reply_markup=MARKUP
        )
        BOT.edit_message_reply_markup(message.chat.id, message.message_id)
    else:
        BOT.send_message(message.chat.id, "В базе данных нет видео.", reply_markup=MARKUP)


@logger.catch
def add_channel(message, channel_url):
    """Функция Добавляет новый канала в БД"""
    picture = get_pictures()
    MARKUP = get_back_keyboard()
    try:
        if (
            channel_url.startswith("https://www.youtube.com/")
            or channel_url.startswith("https://youtube.com/")
            and 0 < int(message.text) <= 10
        ):
            BOT.send_photo(
                message.chat.id,
                photo=picture['ERIC_THINKING'],
                caption="Я думаю...",
            )
            channel_name, channel_rating = check_channel_data(message, channel_url)
            channel = Channel.objects.all().filter(title=channel_name)

            if not channel.exists():
                Channel.objects.create(
                    title=channel_name,
                    url=channel_url,
                    rating=channel_rating
                )
                
                BOT.send_message(
                    message.chat.id,
                    f"~~Канал '{channel_name}' добавлен в базу.~~",
                    reply_markup=MARKUP,
                )
            else:
                BOT.send_message(message.chat.id, "~~Канал уже есть в базе.~~", reply_markup=MARKUP)
    except:
        BOT.send_message(message.chat.id, "~~Вы ввели неправильные данные.~~")
        

@logger.catch
def delete_channel(message):
    """Функция удаляет канал из базы данных"""
    channel_name = message.text
    channel = Channel.objects.all().filter(title=channel_name)
    
    if channel.exists():
        channel.delete()
        BOT.send_message(message.chat.id, f"~~Канал '{channel_name}' удалён.~~")
    else:
        BOT.send_message
        (message.chat.id, "~~В вашей базе нет такого канала, начните заново.~~")


@logger.catch
def show_all_channels(message):
    """Функция показывает все имеющиеся каналы в БД"""
    channels = Channel.objects.all().order_by('-rating')
    MARKUP = get_show_channels_keyboard()
    if channels.exists():
        BOT.send_message(message.chat.id, "~~Список всех каналов:~~\n")
        for name in channels:
            BOT.send_message(message.chat.id, f"{name}" )
        BOT.send_message(
            message.chat.id,
            "~~Список окончен. Выберите действие:~~",
            reply_markup=MARKUP,
        )
    else:
        BOT.send_message(message.chat.id, "~~У вас не добавлены каналы.~~")
        BOT.register_next_step_handler(message, MARKUP)



@logger.catch
def add_new_video(message):
    """Функция добавляет новое видео в БД"""
    picture = get_pictures()
    if message.text.startswith(
        "https://www.youtube.com/watch"
    ) or message.text.startswith("https://youtu.be/"):
        BOT.send_photo(
            message.chat.id, photo=picture['ERIC_THINKING'], caption="Я думаю..."
        )
        sleep(1.5)
        channel_name, video_url = check_video_data(message)
        channel_rating = Channel.objects.all().filter(title=channel_name).values_list('rating')
        try:
            if Video.objects.filter(url=video_url).exists():
                BOT.send_message(
                message.chat.id, "~~Это видео уже есть в базе~~"
            )
            elif channel_rating.exists():
                Video.objects.create(
                    video_channel_name=channel_name,
                    url=video_url,
                    video_rating=channel_rating
                )
                BOT.send_message(message.chat.id, "~~Видео добавлено.~~")
            else:
                Video.objects.create(
                    video_channel_name=channel_name,
                    url=video_url
                )
                BOT.send_message(message.chat.id, "~~Видео добавлено.~~")
        except:
            BOT.send_message(
                message.chat.id, "~~Вы отправили неверную ссылку, начните сначала.~~"
            )


class Command(BaseCommand):
    help = "Телеграм-бот"

    @BOT.message_handler(func=lambda message: True, content_types=['text'])
    def handle(self, *args, **options):
        sleep(3)
        print(BOT.get_me())
        while True:
            try:
                thread1 = threading.Thread(target=BOT.polling(none_stop=True))
                thread1.start()
            except Exception as error:
                logger.error(error)
                BOT.send_message(TELEGRAM_CHAT_ID, f"Error at startup {error}")
                sleep(10)
