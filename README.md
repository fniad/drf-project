# Online Learning Platform

##  Описание
Проект "Online Learning Platform" – это современная система управления обучением (LMS), предназначенная для создания, публикации и прохождения онлайн-курсов. Основанный на концепции Single Page Application (SPA), проект предлагает эффективный и удобный интерфейс пользователя для обучения в любое удобное время.

## Стек технологий

Бэкенд построен на Django с использованием Django Rest Framework для создания API. Celery используется для асинхронной обработки задач, а Redis — в качестве брокера сообщений.

## Установка через DOCKER

### Шаг 1. Клонирование репозитория

1. ```git clone https://github.com/fniad/online_learning_platform.git```
2. ```cd online_learning_platform```

### Шаг 2. Настройка окружения

1. ```touch .env.docker``` 
2. ```nano .env.docker``` и заполнить по шаблону из .env.docker.test

### Шаг 3. На Ubuntu или Linux сначала остановить postgresql

```systemctl stop postgresql```

### Шаг 4. Запуск docker-compose

1. ```docker-compose build```
2. ```docker-compose exec app python manage.py migrate``` в соседнем терминале
3. ```docker-compose up```
