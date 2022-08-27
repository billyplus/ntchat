import os
import logging
from datetime import datetime
from .xdg import get_log_dir
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

    # create file handler and set level to debug
    if conf.LOG_FILE_KEY in os.environ:
        filepath = os.environ[conf.LOG_FILE_KEY]
    else:
        base_dir = get_log_dir()
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        time_now = datetime.now()
        time_format = '%Y-%m-%d-%H-%M'

        filepath = f'{base_dir}/log-{time_now.strftime(time_format)}.txt'

    file_handler = logging.FileHandler(filepath, 'a', encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger
