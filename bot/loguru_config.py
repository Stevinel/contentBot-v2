from loguru import logger

logger.add(
    "bot_debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
)
