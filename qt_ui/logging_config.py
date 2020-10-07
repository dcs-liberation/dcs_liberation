"""Logging APIs."""
import logging
import os
from logging.handlers import RotatingFileHandler


def init_logging(version: str) -> None:
    """Initializes the logging configuration."""
    if not os.path.isdir("./logs"):
        os.mkdir("logs")

    fmt = "%(asctime)s :: %(levelname)s :: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    logger = logging.getLogger()

    handler = RotatingFileHandler('./logs/liberation.log', 'a', 5000000, 1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(fmt))

    logger.addHandler(handler)

    logger.info(f"DCS Liberation {version}")
