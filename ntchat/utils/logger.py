import logging
import os
import configparser
from datetime import datetime
from .xdg import get_log_dir, get_exec_dir

NTCHAT_LOG_KEY = 'NTCHAT_LOG'
NTCHAT_LOG_FILE_KEY = 'NTCHAT_LOG_FILE'


config_file = os.path.join(get_exec_dir(), "config.ini")
CONFIG_DEBUG_LEVEL = ''

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    CONFIG_DEBUG_LEVEL = config.get('Config', 'LogLevel', fallback=CONFIG_DEBUG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """
    configured Loggers
    """
    NTCHAT_LOG = os.environ.get(NTCHAT_LOG_KEY, 'DEBUG')
    log_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if CONFIG_DEBUG_LEVEL:
        NTCHAT_LOG = CONFIG_DEBUG_LEVEL

    # create logger and set level to debug
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(NTCHAT_LOG)
    logger.propagate = False

    # create file handler and set level to debug
    if NTCHAT_LOG_FILE_KEY in os.environ:
        filepath = os.environ[NTCHAT_LOG_FILE_KEY]
    else:
        base_dir = get_log_dir()
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        time_now = datetime.now()
        time_format = '%Y-%m-%d-%H-%M'

        filepath = f'{base_dir}/log-{time_now.strftime(time_format)}.txt'

    file_handler = logging.FileHandler(filepath, 'a', encoding='utf-8')
    file_handler.setLevel(NTCHAT_LOG)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(NTCHAT_LOG)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger
