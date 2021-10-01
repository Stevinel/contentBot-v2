"""Здесь хранятся ссылки, по которым будут делаться запросы к yotubeAPI"""


GET_CHANNEL_BY_USERNAME = (
    "https://youtube.googleapis.com/youtube/v3/" "channels?part=snippet&forUsername="
)
GET_CHANNEL_BY_ID = "https://youtube.googleapis.com/youtube/v3/channels?part=snippet&id="
SEARCH_VIDEO_BY_CHANNEL_ID = (
    "https://www.googleapis.com/youtube/v3/" "search?order=date&part=snippet&channelId="
)
SEARCH_BROKEN_CHANNEL = (
    "https://youtube.googleapis.com/youtube/v3/" "search?part=snippet&maxResults=5&q="
)
GET_CHANNEL_ID_FROM_VIDEO = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id="
YOUTUBE_URL = "https://www.youtube.com/watch?v="
