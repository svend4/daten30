# Termux Setup Guide - Команды для всех сценариев

Это руководство содержит команды Termux для трех различных уровней приложений:
1. **Демо-приложение** - простое приложение для обучения
2. **Hub Portal** - динамический портал с микросервисами
3. **Production приложение** - полноценное приложение с расширенным стеком

---

## 📱 Сценарий 1: Демо-приложение (demo-app)

### Описание
Простое микросервисное приложение с 3 сервисами: user, product, order.
Минимальный стек для обучения и быстрого старта.

### Шаг 1: Установка базовых пакетов

```bash
# Обновление пакетов Termux
pkg update && pkg upgrade -y

# Установка Python
pkg install python -y

# Установка Git
pkg install git -y

# Установка утилит
pkg install wget curl -y
```

### Шаг 2: Клонирование репозитория

```bash
# Переход в домашнюю директорию
cd ~

# Клонирование репозитория
git clone <URL_репозитория> daten30

# Переход в директорию проекта
cd daten30/demo-app/backend-flask
```

### Шаг 3: Установка Python зависимостей

```bash
# Установка pip зависимостей для всех сервисов
pip install flask flask-cors

# Альтернатива: использовать requirements.txt
pip install -r requirements.txt
```

### Шаг 4: Запуск демо-приложения

```bash
# Запуск User Service (порт 5001)
cd ~/daten30/demo-app/backend-flask/user-service
python user_service.py &

# Запуск Product Service (порт 5002)
cd ~/daten30/demo-app/backend-flask/product-service
python product_service.py &

# Запуск Order Service (порт 5003)
cd ~/daten30/demo-app/backend-flask/order-service
python order_service.py &
```

### Шаг 5: Проверка работы

```bash
# Проверка User Service
curl http://127.0.0.1:5001/api/users

# Проверка Product Service
curl http://127.0.0.1:5002/api/products

# Проверка Order Service
curl http://127.0.0.1:5003/api/orders
```

### Остановка сервисов

```bash
# Найти процессы Python
ps aux | grep python

# Остановить все процессы Python
pkill -f python
```

---

## 🔌 Сценарий 2: Hub Portal (динамический портал с микросервисами)

### Описание
Динамический портал с Service Registry, Message Bus и 5 микросервисами-плагинами.
Архитектура "скелет + игрушки" с автоматическим обнаружением сервисов.

### Шаг 1: Установка базовых пакетов

```bash
# Обновление пакетов Termux
pkg update && pkg upgrade -y

# Установка Python и pip
pkg install python -y

# Установка Git
pkg install git -y

# Установка SQLite (для баз данных)
pkg install sqlite -y

# Установка утилит
pkg install wget curl jq -y
```

### Шаг 2: Клонирование репозитория

```bash
# Переход в домашнюю директорию
cd ~

# Клонирование репозитория
git clone <URL_репозитория> daten30

# Переход в директорию hub-portal
cd daten30/hub-portal
```

### Шаг 3: Установка Python зависимостей

```bash
# Установка всех необходимых зависимостей
pip install flask flask-cors requests

# Для Product Service (SQLite)
pip install sqlite3

# Проверка установки
pip list | grep -i flask
```

### Шаг 4: Запуск инфраструктурных сервисов

```bash
# Запуск Service Registry (порт 5000) - ОБЯЗАТЕЛЬНО ПЕРВЫМ!
cd ~/daten30/hub-portal/infrastructure/registry-service
python registry_service.py &

# Подождать 2 секунды
sleep 2

# Запуск Message Bus (порт 5999)
cd ~/daten30/hub-portal/infrastructure/message-bus
python message_bus.py &

# Подождать 2 секунды
sleep 2
```

### Шаг 5: Запуск микросервисов (плагинов)

```bash
# Product Service (порт 5001)
cd ~/daten30/hub-portal/microservices/product-service
python product_service.py &
sleep 1

# Weather Service (порт 5002)
cd ~/daten30/hub-portal/microservices/weather-service
python weather_service.py &
sleep 1

# Crypto Service (порт 5003)
cd ~/daten30/hub-portal/microservices/crypto-service
python crypto_service.py &
sleep 1

# News Service (порт 5004)
cd ~/daten30/hub-portal/microservices/news-service
python news_service.py &
sleep 1

# Task Service (порт 5005)
cd ~/daten30/hub-portal/microservices/task-service
python task_service.py &
sleep 1
```

### Шаг 6: Автоматический запуск всех сервисов

```bash
# Использование скрипта автозапуска
cd ~/daten30/hub-portal
bash scripts/start-all.sh

# Проверка здоровья всех сервисов
bash scripts/health-check.sh
```

### Шаг 7: Проверка работы Hub Portal

```bash
# Проверка Service Registry
curl http://127.0.0.1:5000/api/services | jq

# Проверка Message Bus
curl http://127.0.0.1:5999/api/events | jq

# Проверка Product Service
curl http://127.0.0.1:5001/api/products | jq

# Проверка Weather Service
curl http://127.0.0.1:5002/api/weather/current/Moscow | jq

# Проверка Crypto Service
curl http://127.0.0.1:5003/api/crypto/prices | jq

# Проверка News Service
curl http://127.0.0.1:5004/api/news | jq

# Проверка Task Service
curl http://127.0.0.1:5005/api/tasks | jq
```

### Остановка Hub Portal

```bash
# Использование скрипта остановки
cd ~/daten30/hub-portal
bash scripts/stop-all.sh

# Альтернатива: остановить все процессы Python
pkill -f python
```

---

## 🚀 Сценарий 3: Production приложение (расширенный стек)

### Описание
Полноценное production-ready приложение с PostgreSQL, Redis, RabbitMQ, Docker, Nginx.
Максимальная функциональность и производительность.

### Шаг 1: Установка базовых пакетов

```bash
# Обновление пакетов Termux
pkg update && pkg upgrade -y

# Установка основных языков программирования
pkg install python nodejs-lts golang rust -y

# Установка баз данных
pkg install postgresql redis sqlite -y

# Установка утилит
pkg install git wget curl jq nginx -y

# Установка инструментов разработки
pkg install make cmake clang -y
```

### Шаг 2: Настройка PostgreSQL

```bash
# Инициализация PostgreSQL
initdb $PREFIX/var/lib/postgresql

# Запуск PostgreSQL
pg_ctl -D $PREFIX/var/lib/postgresql start

# Создание пользователя и базы данных
createuser -s postgres
createdb hub_portal_db

# Проверка подключения
psql -U postgres -d hub_portal_db -c "SELECT version();"
```

### Шаг 3: Настройка Redis

```bash
# Запуск Redis
redis-server --daemonize yes

# Проверка работы Redis
redis-cli ping
# Ответ: PONG
```

### Шаг 4: Установка RabbitMQ (через Docker)

```bash
# ВНИМАНИЕ: Docker в Termux требует proot-distro

# Установка proot-distro
pkg install proot-distro -y

# Установка Ubuntu в proot
proot-distro install ubuntu

# Вход в Ubuntu
proot-distro login ubuntu

# В Ubuntu: установка Docker (альтернатива)
# Или использовать RabbitMQ через Python
pip install pika

# Выход из proot
exit
```

### Шаг 5: Установка Python зависимостей (расширенный набор)

```bash
# Веб-фреймворки
pip install flask fastapi uvicorn gunicorn

# CORS и безопасность
pip install flask-cors python-jose passlib bcrypt

# Базы данных
pip install psycopg2-binary redis pymongo

# Очереди сообщений
pip install pika celery

# ORM и миграции
pip install sqlalchemy alembic

# Валидация данных
pip install pydantic marshmallow

# HTTP клиенты
pip install requests httpx aiohttp

# Мониторинг
pip install prometheus-client

# Тестирование
pip install pytest pytest-cov

# Утилиты
pip install python-dotenv click
```

### Шаг 6: Настройка Node.js сервисов

```bash
# Установка глобальных пакетов
npm install -g pm2 nodemon

# Установка зависимостей для Node.js микросервисов
cd ~/daten30/hub-portal/microservices/nodejs-service
npm install express cors body-parser axios

# Установка TypeScript (опционально)
npm install -g typescript ts-node
```

### Шаг 7: Настройка Go сервисов

```bash
# Установка Go модулей
cd ~/daten30/hub-portal/microservices/go-service
go mod init github.com/yourname/go-service
go get github.com/gin-gonic/gin
go get github.com/lib/pq
go get github.com/go-redis/redis/v8
```

### Шаг 8: Настройка Nginx (reverse proxy)

```bash
# Создание конфигурации Nginx
cat > $PREFIX/etc/nginx/nginx.conf << 'EOF'
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    upstream registry {
        server 127.0.0.1:5000;
    }

    upstream message_bus {
        server 127.0.0.1:5999;
    }

    server {
        listen 8080;
        server_name localhost;

        location /registry/ {
            proxy_pass http://registry/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /bus/ {
            proxy_pass http://message_bus/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# Запуск Nginx
nginx

# Проверка Nginx
curl http://127.0.0.1:8080/registry/api/services
```

### Шаг 9: Настройка переменных окружения

```bash
# Создание .env файла
cat > ~/daten30/.env << 'EOF'
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/hub_portal_db

# Redis
REDIS_URL=redis://localhost:6379

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# JWT
JWT_SECRET_KEY=your-secret-key-change-this

# Registry
REGISTRY_URL=http://127.0.0.1:5000

# Message Bus
MESSAGE_BUS_URL=http://127.0.0.1:5999

# Environment
ENVIRONMENT=production
DEBUG=false
EOF
```

### Шаг 10: Запуск production приложения

```bash
# Запуск PostgreSQL
pg_ctl -D $PREFIX/var/lib/postgresql start

# Запуск Redis
redis-server --daemonize yes

# Запуск Nginx
nginx

# Запуск Service Registry с Gunicorn
cd ~/daten30/hub-portal/infrastructure/registry-service
gunicorn -w 4 -b 127.0.0.1:5000 registry_service:app --daemon

# Запуск Message Bus с Gunicorn
cd ~/daten30/hub-portal/infrastructure/message-bus
gunicorn -w 4 -b 127.0.0.1:5999 message_bus:app --daemon

# Запуск микросервисов с PM2 (для Node.js)
cd ~/daten30/hub-portal/microservices/nodejs-service
pm2 start server.js --name "nodejs-service"

# Запуск Python микросервисов с Gunicorn
cd ~/daten30/hub-portal/microservices/product-service
gunicorn -w 2 -b 127.0.0.1:5001 product_service:app --daemon

cd ~/daten30/hub-portal/microservices/weather-service
gunicorn -w 2 -b 127.0.0.1:5002 weather_service:app --daemon

cd ~/daten30/hub-portal/microservices/crypto-service
gunicorn -w 2 -b 127.0.0.1:5003 crypto_service:app --daemon

cd ~/daten30/hub-portal/microservices/news-service
gunicorn -w 2 -b 127.0.0.1:5004 news_service:app --daemon

cd ~/daten30/hub-portal/microservices/task-service
gunicorn -w 2 -b 127.0.0.1:5005 task_service:app --daemon
```

### Шаг 11: Мониторинг production приложения

```bash
# Проверка процессов
ps aux | grep -E "gunicorn|nginx|postgres|redis"

# Проверка PM2
pm2 list

# Проверка логов
pm2 logs

# Проверка Gunicorn логов
tail -f /tmp/gunicorn-*.log

# Проверка Nginx логов
tail -f $PREFIX/var/log/nginx/access.log
tail -f $PREFIX/var/log/nginx/error.log

# Проверка PostgreSQL
psql -U postgres -d hub_portal_db -c "SELECT * FROM services;"

# Проверка Redis
redis-cli
> KEYS *
> GET some_key
> EXIT
```

### Шаг 12: Создание скрипта автозапуска production

```bash
# Создание скрипта start-production.sh
cat > ~/daten30/start-production.sh << 'EOF'
#!/bin/bash

echo "Starting production stack..."

# Start PostgreSQL
echo "Starting PostgreSQL..."
pg_ctl -D $PREFIX/var/lib/postgresql start

# Start Redis
echo "Starting Redis..."
redis-server --daemonize yes

# Start Nginx
echo "Starting Nginx..."
nginx

# Wait for databases
sleep 3

# Start Service Registry
echo "Starting Service Registry..."
cd ~/daten30/hub-portal/infrastructure/registry-service
gunicorn -w 4 -b 127.0.0.1:5000 registry_service:app --daemon

# Start Message Bus
echo "Starting Message Bus..."
cd ~/daten30/hub-portal/infrastructure/message-bus
gunicorn -w 4 -b 127.0.0.1:5999 message_bus:app --daemon

# Wait for infrastructure
sleep 3

# Start microservices
echo "Starting microservices..."
cd ~/daten30/hub-portal/microservices/product-service
gunicorn -w 2 -b 127.0.0.1:5001 product_service:app --daemon

cd ~/daten30/hub-portal/microservices/weather-service
gunicorn -w 2 -b 127.0.0.1:5002 weather_service:app --daemon

cd ~/daten30/hub-portal/microservices/crypto-service
gunicorn -w 2 -b 127.0.0.1:5003 crypto_service:app --daemon

cd ~/daten30/hub-portal/microservices/news-service
gunicorn -w 2 -b 127.0.0.1:5004 news_service:app --daemon

cd ~/daten30/hub-portal/microservices/task-service
gunicorn -w 2 -b 127.0.0.1:5005 task_service:app --daemon

echo "Production stack started!"
echo "Registry: http://127.0.0.1:5000"
echo "Nginx proxy: http://127.0.0.1:8080"
EOF

# Сделать исполняемым
chmod +x ~/daten30/start-production.sh
```

### Остановка production приложения

```bash
# Остановка всех Gunicorn процессов
pkill -f gunicorn

# Остановка PM2
pm2 stop all

# Остановка Nginx
nginx -s stop

# Остановка Redis
redis-cli shutdown

# Остановка PostgreSQL
pg_ctl -D $PREFIX/var/lib/postgresql stop
```

---

## 📊 Сравнение команд для трех сценариев

| Компонент | Демо-приложение | Hub Portal | Production |
|-----------|----------------|------------|-----------|
| **Python пакеты** | `flask flask-cors` | `flask flask-cors requests` | `flask fastapi gunicorn psycopg2 redis celery` |
| **Базы данных** | Нет | `sqlite` | `postgresql redis sqlite` |
| **Веб-сервер** | Flask dev server | Flask dev server | `nginx gunicorn` |
| **Процессы** | 3 сервиса | 7 сервисов | 10+ сервисов |
| **Автозапуск** | Ручной | `start-all.sh` | `start-production.sh` |
| **Мониторинг** | `curl` | `health-check.sh` | `pm2 logs`, PostgreSQL, Redis CLI |

---

## 🎯 Быстрый старт для каждого сценария

### Демо-приложение (5 минут)
```bash
pkg update && pkg install python git -y
pip install flask flask-cors
cd ~/daten30/demo-app/backend-flask
# Запустить 3 сервиса вручную
```

### Hub Portal (10 минут)
```bash
pkg update && pkg install python git sqlite -y
pip install flask flask-cors requests
cd ~/daten30/hub-portal
bash scripts/start-all.sh
```

### Production (30+ минут)
```bash
pkg update && pkg install python nodejs postgresql redis nginx git -y
pip install flask fastapi gunicorn psycopg2-binary redis
# Настроить PostgreSQL, Redis, Nginx
bash ~/daten30/start-production.sh
```

---

## 🔧 Полезные команды для всех сценариев

### Проверка портов
```bash
# Посмотреть какие порты заняты
netstat -tlnp | grep LISTEN

# Найти процесс на определенном порту
lsof -i :5000
```

### Очистка процессов
```bash
# Убить все Python процессы
pkill -f python

# Убить процесс по PID
kill -9 <PID>

# Убить все процессы на порту
fuser -k 5000/tcp
```

### Логирование
```bash
# Перенаправить вывод в файл
python service.py > service.log 2>&1 &

# Просмотр логов в реальном времени
tail -f service.log

# Поиск ошибок в логах
grep -i error service.log
```

### Автозапуск при старте Termux
```bash
# Добавить в ~/.bashrc
echo "cd ~/daten30/hub-portal && bash scripts/start-all.sh" >> ~/.bashrc
```

---

## 📝 Примечания

1. **Демо-приложение** - идеально для обучения и экспериментов
2. **Hub Portal** - оптимальное решение для Termux, баланс функциональности и простоты
3. **Production** - для серьезных приложений, требует больше ресурсов

Рекомендуется начинать с **Hub Portal** (сценарий 2), так как он предоставляет мощную архитектуру при минимальных требованиях.
