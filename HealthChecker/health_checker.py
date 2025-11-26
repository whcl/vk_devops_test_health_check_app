import requests
from logger import logger
import docker


class HealthChecker:
    """
    Класс для мониторинга и управления здоровьем приложения.

    Осуществляет проверку доступности приложения и автоматический перезапуск при необходимости.
    """

    def __init__(self, app_url: str, app_port: int):
        """
        Инициализирует HealthChecker с URL и портом приложения.

        Args:
            app_url: URL приложения для мониторинга
            app_port: Порт приложения для мониторинга
        """
        self.app_url = app_url
        self.app_port = app_port
        self.docker_client = docker.from_env()

    @logger()
    def check_availability(self) -> dict:
        """
        Проверяет доступность сервера и возвращает подробную информацию.

        Returns:
            Словарь с информацией о статусе, содержащий:
                - status_code: HTTP статус-код ответа
                - url: URL приложения
                - port: Порт приложения
                - response_time: Время ответа в секундах
                - message: Текстовое описание статуса
        """
        try:
            response = requests.get(f'http://{self.app_url}:{self.app_port}')

            result = {
                "status_code": response.status_code,
                "url": self.app_url,
                "port": self.app_port,
                "response_time": response.elapsed.total_seconds(),
                "message": "Сервер доступен" if response.status_code == 200 else f"Статус: {response.status_code}"
            }
            return result
        except Exception as e:
            # При ошибке подключения выполняем перезапуск приложения
            self.reboot_app()

    @logger()
    def reboot_app(self):
        """
        Выполняет перезапуск Docker контейнера приложения.

        Получает контейнер по имени и выполняет его restart.
        """
        container = self.docker_client.containers.get(self.app_url)
        container.restart()