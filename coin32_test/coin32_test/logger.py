import logging
import os
import traceback

from django.conf import settings

from shortener.constants import LOG_PATH

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# todo Не очень было понятно, что поздразумевается под "Логированием"
#  (каким способом (БД, файл, Sentry и т.д.) и какие события логировать.
#  Добавил логирование в текстовый файл некоторых событый из Views + добавлен
#  декоратор log_on_exception для отлова каких-либо исключений.


loggers = [('error_logger', logging.ERROR, 'error.log'),
           ('info_logger', logging.INFO, 'info.log')]


formatter = logging.Formatter("[%(asctime)s] %(message)s")
formatter.datefmt = '%Y-%m-%d %H:%M:%S'
for logger_name, logger_level, file_name in loggers:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)
    handler = logging.FileHandler(os.path.join(LOG_PATH, file_name))
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_info(msg, request=None):
    log = logging.getLogger('info_logger')
    if request:
        msg = f'{msg} | Session Key: {request.session.session_key}'
    log.info(msg)


def log_error(msg, request=None):
    log = logging.getLogger('error_logger')
    if request:
        msg = f'{msg} Session Key: {request.session.session_key}'
    log.error(msg)


def log_on_exception(func):
    """
    Декоратор логирующий ошибки в лог файл при выполнении функции.
    """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception:
            log_error(traceback.format_exc())
            if settings.DEBUG:
                raise
        else:
            return result

    return wrapper
