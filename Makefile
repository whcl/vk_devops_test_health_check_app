# Переменная для интервала проверки здоровья (в секундах)
INTERVAL ?= 5

# Сборка и запуск всех сервисов с указанным интервалом
install:
	HEALTH_CHECK_INTERVAL=$(INTERVAL) docker-compose up --build

# Остановка всех сервисов
stop:
	docker-compose down

# Обновление сервисов (остановка, пересборка и запуск)
update:
	docker-compose down
	HEALTH_CHECK_INTERVAL=$(INTERVAL) docker-compose up --build

# Полная очистка (остановка сервисов и удаление volumes)
clean:
	docker-compose down -v --remove-orphans