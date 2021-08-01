"""Logging APIs."""
import logging
import os
from logging.handlers import RotatingFileHandler

from qt_ui.logging_handler import HookableInMemoryHandler


def init_logging(version: str) -> None:
    """Initializes the logging configuration."""
    if not os.path.isdir("./logs"):
        os.mkdir("logs")

    fmt = "%(asctime)s :: %(levelname)s :: %(message)s"
    formatter = logging.Formatter(fmt)

    logging.basicConfig(level=logging.DEBUG, format=fmt)
    logger = logging.getLogger()

    rotating_file_handler = RotatingFileHandler(
        "./logs/liberation.log", "a", 5000000, 1
    )
    rotating_file_handler.setLevel(logging.DEBUG)
    rotating_file_handler.setFormatter(formatter)

    hookable_in_memory_handler = HookableInMemoryHandler()
    hookable_in_memory_handler.setLevel(logging.DEBUG)
    hookable_in_memory_handler.setFormatter(formatter)

    logger.addHandler(rotating_file_handler)
    logger.addHandler(hookable_in_memory_handler)

    logger.info(f"DCS Liberation {version}")
