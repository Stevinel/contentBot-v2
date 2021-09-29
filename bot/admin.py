from django.contrib import admin

from .models import Channel, Video

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "url", "rating")
    search_fields = ("title",)
    list_filter = ("rating",)
    empty_value_display = "-пусто-"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("pk", "video_channel_name", "url", "video_rating")
    search_fields = ("url", "video_channel_name")
    list_filter = ("video_rating", "video_channel_name")
    empty_value_display = "-пусто-"
