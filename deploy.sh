# Установка зависимостей
poetry install &&
# Применение миграций
poetry run python3 manage.py migrate &&
# Сбор статики
poetry run python3 manage.py collectstatic --no-input
