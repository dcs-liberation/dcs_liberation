import logging
import os
from logging.handlers import RotatingFileHandler


def init_logging(version_string):
    if not os.path.isdir("./logs"):
        os.mkdir("logs")

    logging.basicConfig(level="DEBUG")
    logger = logging.getLogger()

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    handler = RotatingFileHandler('./logs/liberation.log', 'a', 5000000, 1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(handler)

    logger.info("DCS Liberation {}".format(version_string))
