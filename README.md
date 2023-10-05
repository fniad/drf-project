# drf-project

### Шаг 1. Клонирование репозитория

```git clone https://github.com/fniad/drf-project.git```

```cd drf-project```

### Шаг 2. Установка зависимостей

```python3 poetry install```

```poetry shell```

### Шаг 3. Установка и настройка PostgreSQL

```sudo apt-get install postgresql```

```sudo -u postgres psql```

```CREATE DATABASE drf_project;```

```\q```

### Шаг 4. Настройка окружения

```touch .env```

```nano .env```

и заполнить по шаблону из **.env.test**

### Шаг 5. Загрузка данных с помощью команд 

1. ```python3 manage.py fill_db``` (загрузка в БД данных по платежам)

### Шаг 6 Применение миграций

```python3 manage.py migrate```
