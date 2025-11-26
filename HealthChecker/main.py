import os
import time

from health_checker import HealthChecker


def get_env_variable(name: str, default: str = None) -> str:
    """
    Получает значение переменной окружения.

    Args:
        name: Имя переменной окружения
        default: Значение по умолчанию, если переменная не установлена

    Returns:
        Значение переменной окружения или значение по умолчанию

    Raises:
        ValueError: Если переменная не установлена и нет значения по умолчанию
    """
    value = os.getenv(name)
    if value is not None:
        return value
    elif default is not None:
        return default
    else:
        raise ValueError(f"Environment variable {name} is required")


def main():
    """
    Основная функция для запуска периодической проверки состояния.
    """
    app_name = get_env_variable("APP_NAME", "vk_devops_test")
    app_port = get_env_variable("APP_PORT", "8000")
    check_interval = int(get_env_variable("HEALTH_CHECK_INTERVAL", "5"))



    # Создаем экземпляр HealthChecker
    checker = HealthChecker(
        app_url=app_name,
        app_port=app_port,
    )

    try:
        while True:
            checker.check_availability()
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n Health checker stopped")


if __name__ == "__main__":
    main()