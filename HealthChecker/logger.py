import logging
import os
import functools
from typing import Optional


def logger(log_dir: Optional[str] = None):
    """
    Декоратор для логирования вызовов функций.

    Логирует начало выполнения, успешное завершение и ошибки функции.
    Использует файловое и консольное логирование.

    Args:
        log_dir: Директория для логов. Если None, используется LOG_DIR из env или './logs'

    Returns:
        Декорированную функцию с логированием
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            final_log_dir = log_dir or os.getenv('LOG_DIR', './logs')

            os.makedirs(final_log_dir, exist_ok=True)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            log_file = os.path.join(final_log_dir, 'app.log')

            file_handler = logging.FileHandler(log_file, 'a')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)

            logger_name = func.__module__ + '.' + func.__name__
            logger = logging.getLogger(logger_name)
            logger.propagate = False
            logger.setLevel(logging.INFO)
            logger.handlers.clear()

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            try:

                logger.info(f"Starting method: {func.__name__}")

                result = func(*args, **kwargs)

                logger.info(f"Method {func.__name__} completed successfully. Result: {result}")

                return result
            except Exception as e:

                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise
            finally:

                for handler in logger.handlers:
                    handler.close()
                logger.handlers.clear()

        return wrapper

    return decorator
