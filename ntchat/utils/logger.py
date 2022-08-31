import os
import logging
from .. import conf


def get_logger(name: str) -> logging.Logger:
    """
    configured Loggers
    """
    log_level = os.environ.get(conf.LOG_KEY, conf.LOG_LEVEL)
    log_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create logger and set level to debug
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(log_level)
    logger.propagate = False

    # create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger
