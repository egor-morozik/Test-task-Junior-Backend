# Instagram Content Sync Service

## Стек
* **Python 3.14** 
* **Django 6.0 + DRF** 
* **PostgreSQL**
* **Docker & Docker Compose V2** 
* **Pytest + Pytest-Django** 
* **Mypy**
* **UV**

## Архитектура 

* **Clients (`core/clients.py`)**: Инкапсулируют логику HTTP-запросов к Instagram API. Обрабатывают ошибки сети и проверяют статус-коды ответов.
* **Services (`core/services.py`)**: Слой бизнес-логики. Здесь реализована синхронизация, обход пагинации через генераторы и логика обновления данных.
* **Serializers (`core/serializers.py`)**: Отвечают за валидацию входящих данных и маппинг полей внешнего API на внутренние модели.
* **Views (`core/views.py`)**: Контроллеры, которые делегируют выполнение задач сервисному слою.

## Установка и запуск

**Клонируйте репозиторий:**
```bash
git clone https://github.com/egor-morozik/Test-task-Junior-Backend
```
**Настройте переменные окружения:**  
Скопируйте пример конфига и подставьте ваш токен из App Dashboard:
```bash
cp .env.example .env
```  
Заполните INSTAGRAM_ACCESS_TOKEN в .env.  

**Запустите проект:**  
Используйте Docker Compose:
```bash
docker-compose up --build
```
Рекомендуется V2:
```bash
docker compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

**API Endpoints**  

POST http://localhost:8000/api/sync/ — запуск полной синхронизации постов и комментариев из Instagram.  

GET http://localhost:8000/api/posts/ — список постов из БД (используется CursorPagination).  

POST http://localhost:8000/api/posts/{id}/comment/ — отправка комментария в Instagram и сохранение в локальную БД.

## Тестирование и качество кода
**Интеграционные тесты**  

Написаны тесты для эндпоинта создания комментария, покрывающие:
- Успешное создание записи в БД и корректный ответ API.
- Обработку ошибки 404, если пост отсутствует в локальной базе.
- Обработку ошибки 400, если пост удален в самом Instagram


Запуск тестов в контейнере:  
```bash
docker-compose exec backend uv run pytest
```
V2:  
```bash
docker compose exec backend uv run pytest
```

**Статическая типизация**  
Проект покрыт Type Hinting. Проверка типов с помощью mypy.  

**Литнеры и форматтеры**  
Использовался ruff
