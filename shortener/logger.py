import logging
import os
import traceback

from .constants import LOG_PATH

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# todo Не очень было понятно, что поздразумевается под "Логированием"
#  (каким способом (БД, файл, Sentry и т.д.) и какие события логировать.
#  Добавил логирование в текстовый файл некоторых событый из Views + добавлен
#  декоратор log_on_exception для отлова каких-либо исключений.

logger = logging.getLogger('shortener_logger')

logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(LOG_PATH, 'errors.log'))
formatter = logging.Formatter("[%(asctime)s] %(message)s")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def log_on_exception(func):
    """
    Декоратор логирующий ошибки в лог файл при выполнении функции.
    """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception:
            logger.error(traceback.format_exc())
        else:
            return result

    return wrapper
