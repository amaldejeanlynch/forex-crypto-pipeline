# src/utils/logger.py

import logging
from config import LogConfig, PathConfig
import os


def setup_logger(name):
    # Create log directory if it doesn't exist
    os.makedirs(PathConfig.LOG_DIR, exist_ok=True)

    # Same as before - just using config values
    logging.basicConfig(
        level=logging.INFO,
        format=LogConfig.LOG_FORMAT,
        handlers=[
            logging.FileHandler(LogConfig.LOG_FILE),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)
