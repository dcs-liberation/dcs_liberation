"""Logging APIs."""
import logging
import logging.config
import os
from pathlib import Path

import yaml


def init_logging(version: str) -> None:
    """Initializes the logging configuration."""
    if not os.path.isdir("./logs"):
        os.mkdir("logs")

    resources = Path("resources")
    log_config = resources / "default_logging.yaml"
    if (custom_log_config := resources / "logging.yaml").exists():
        log_config = custom_log_config
    with log_config.open() as log_file:
        logging.config.dictConfig(yaml.safe_load(log_file))

    logging.info(f"DCS Liberation {version}")
