# ContentBot v.2

### «Контент помощник».
Это бот, благодаря которому больше не нужно искать свежий контент для просмотра видео с любимых каналов.

Раз  в две недели мы встречаемся с другом, чтобы выпить немного пива и посмотреть видео, которые искали вручную.
До создания бота, мы находили видео и кидали друг другу в личку с хэштегом #контент, а при встрече искали нужные нам видео, которые мы любим смотреть первостепенно, что в последствии стало надоедать.
Поэтому я решил написать бота, который будет делать всю рутину за нас.

Во время пользования первым ботом дорабатывались ошибки, а потом я решил написать 2 версию на Django, сделать её более структурированной.
Первая версия бота >>> https://github.com/Stevinel/ContentBot

### Что умеет бот?
- Парсить новые видео с любимых каналов через Youtube-Api
- Добавлять/Удалять каналы
- Показывать список всех каналов
- Показывать список всех видео накопленных за время
- Есть возможность добавлять видео вручную со сторонних каналов
- Есть кнопка "Смотреть контент", которая выводит по одному отсортированные по релевантности видео
- Есть возможность отложить видео на потом
- Есть возможность удалить видео после просмотра
- Хранение информации о каналах, видео, их рейтинге в базе данных
- Имеется админка

### В чём плюс?
Теперь, мы можем экономить кучу времени и в целом не заходить на youtube для поиска контента и использовать дополнительные функции бота.
Всё что нам надо - добавить любимые каналы и бот сам соберёт для нас контент и отсортирует.

### Установка
1) Склонируйте репозиторий
   ```
    https://github.com/Stevinel/contentBot-v2/
   ```
2) Добавьте свой .env файл в который укажите переменные
   ```
   TELEGRAM_TOKEN - токен вашего бота
   TELEGRAM_CHAT_ID - ваш телеграм id
   GOOGLE_API_KEY - ваш API-KEY (получить можно в google-cloud-platform) https://console.cloud.google.com/apis/
   Добавьте переменные для базы Postgresql
   DB_ENGINE
   DB_NAME
   POSTGRES_USER
   POSTGRES_PASSWORD
   DB_HOST
   DB_PORT
   
   Либо измените в settings.py DATABASES на сеттинги sqlite3 в settings.py
   DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
      }
    }
   ```
3) Активируйте виртуальное окружение и сделайте миграции и запустите команду:
   python manage.py bot & python manage.py runserver
   
### Дополнительная информация
   - Мой бот развёрнут на сервере
   - Подрублен nginx, gunicorn, ssl
   - Имеется админка

   

### Используемый стек
* [Python]
* [Youtube-API]
* [Selenium-webdriver] - (Устарел, использовался в 1ой версии бота)
* [Telebot]
* [Sqlite3]
* [Postgresql]
* [Loguru]

### Изображение
![image](https://user-images.githubusercontent.com/72396348/134493595-a0afce60-334c-447b-8ae4-5244e602518d.png)
