from django.db import models


class Channel(models.Model):
    title = models.CharField("Название канала", max_length=100)
    url = models.CharField("Ссылка канала", max_length=150)
    rating = models.PositiveBigIntegerField("Рейтинг канала")

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.title


class Video(models.Model):
    video_channel_name = models.CharField("Название канала(из видео)", max_length=100)
    url = models.CharField("Ссылка видео", max_length=150)
    video_rating = models.IntegerField("Рейтинг видео", default=0)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.video_channel_name
