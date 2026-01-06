# Termux Commands Cheatsheet - Шпаргалка команд

Краткий справочник команд для всех трех сценариев.

---

## 🎯 Три сценария - три команды

### Сценарий 1: Demo-App (Демо)
```bash
pkg install python git -y && pip install flask flask-cors && cd ~/daten30/demo-app/backend-flask/user-service && python user_service.py &
```

### Сценарий 2: Hub Portal (Рекомендуется)
```bash
pkg install python git sqlite -y && pip install flask flask-cors requests && cd ~/daten30/hub-portal && bash scripts/start-all.sh
```

### Сценарий 3: Production
```bash
pkg install python postgresql redis nginx -y && pip install flask gunicorn psycopg2-binary && bash ~/daten30/start-production.sh
```

---

## 📱 Сценарий 1: Demo-App

### Установка (5 минут)
```bash
# 1. Обновление Termux
pkg update && pkg upgrade -y

# 2. Установка Python и Git
pkg install python git -y

# 3. Установка Flask
pip install flask flask-cors
```

### Запуск сервисов
```bash
# User Service (порт 5001)
cd ~/daten30/demo-app/backend-flask/user-service
python user_service.py &

# Product Service (порт 5002)
cd ~/daten30/demo-app/backend-flask/product-service
python product_service.py &

# Order Service (порт 5003)
cd ~/daten30/demo-app/backend-flask/order-service
python order_service.py &
```

### Быстрая проверка
```bash
curl http://127.0.0.1:5001/api/users
curl http://127.0.0.1:5002/api/products
curl http://127.0.0.1:5003/api/orders
```

### Остановка
```bash
pkill -f python
```

---

## 🔌 Сценарий 2: Hub Portal

### Установка (10 минут)
```bash
# 1. Обновление Termux
pkg update && pkg upgrade -y

# 2. Установка пакетов
pkg install python git sqlite jq -y

# 3. Установка Python библиотек
pip install flask flask-cors requests
```

### Запуск (автоматический)
```bash
cd ~/daten30/hub-portal
bash scripts/start-all.sh
```

### Запуск (ручной)
```bash
# 1. Service Registry (ПЕРВЫМ!)
cd ~/daten30/hub-portal/infrastructure/registry-service
python registry_service.py &
sleep 2

# 2. Message Bus
cd ~/daten30/hub-portal/infrastructure/message-bus
python message_bus.py &
sleep 2

# 3. Product Service
cd ~/daten30/hub-portal/microservices/product-service
python product_service.py &

# 4. Weather Service
cd ~/daten30/hub-portal/microservices/weather-service
python weather_service.py &

# 5. Crypto Service
cd ~/daten30/hub-portal/microservices/crypto-service
python crypto_service.py &

# 6. News Service
cd ~/daten30/hub-portal/microservices/news-service
python news_service.py &

# 7. Task Service
cd ~/daten30/hub-portal/microservices/task-service
python task_service.py &
```

### Проверка
```bash
# Health check всех сервисов
cd ~/daten30/hub-portal
bash scripts/health-check.sh

# Список сервисов в Registry
curl http://127.0.0.1:5000/api/services | jq

# Проверка каждого сервиса
curl http://127.0.0.1:5001/api/products | jq
curl http://127.0.0.1:5002/api/weather/current/Moscow | jq
curl http://127.0.0.1:5003/api/crypto/prices | jq
curl http://127.0.0.1:5004/api/news | jq
curl http://127.0.0.1:5005/api/tasks | jq
```

### Остановка
```bash
cd ~/daten30/hub-portal
bash scripts/stop-all.sh

# Или
pkill -f python
```

---

## 🚀 Сценарий 3: Production

### Установка (30+ минут)
```bash
# 1. Обновление Termux
pkg update && pkg upgrade -y

# 2. Установка всех пакетов
pkg install python nodejs-lts postgresql redis sqlite nginx git jq -y

# 3. Установка Python библиотек
pip install flask fastapi gunicorn psycopg2-binary redis requests celery uvicorn prometheus-client
```

### Настройка PostgreSQL
```bash
# Инициализация
initdb $PREFIX/var/lib/postgresql

# Запуск
pg_ctl -D $PREFIX/var/lib/postgresql start

# Создание пользователя и БД
createuser -s postgres
createdb hub_portal_db

# Проверка
psql -U postgres -d hub_portal_db -c "SELECT version();"
```

### Настройка Redis
```bash
# Запуск Redis
redis-server --daemonize yes

# Проверка
redis-cli ping
# Ответ: PONG
```

### Создание production скрипта
```bash
cat > ~/daten30/start-production.sh << 'SCRIPT'
#!/bin/bash
echo "🚀 Starting Production Stack..."

# Start databases
pg_ctl -D $PREFIX/var/lib/postgresql start
redis-server --daemonize yes
sleep 3

# Start Nginx
nginx

# Start infrastructure
cd ~/daten30/hub-portal/infrastructure/registry-service
gunicorn -w 4 -b 127.0.0.1:5000 registry_service:app --daemon

cd ~/daten30/hub-portal/infrastructure/message-bus
gunicorn -w 4 -b 127.0.0.1:5999 message_bus:app --daemon
sleep 3

# Start microservices
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

echo "✅ Production stack started!"
SCRIPT

chmod +x ~/daten30/start-production.sh
```

### Запуск
```bash
bash ~/daten30/start-production.sh
```

### Проверка
```bash
# Проверка процессов
ps aux | grep -E "gunicorn|nginx|postgres|redis" | grep -v grep

# Проверка сервисов
curl http://127.0.0.1:5000/api/services | jq

# Проверка баз данных
redis-cli ping
psql -U postgres -d hub_portal_db -c "SELECT COUNT(*) FROM services;"
```

### Остановка
```bash
# Остановка всех процессов
pkill -f gunicorn
nginx -s stop
redis-cli shutdown
pg_ctl -D $PREFIX/var/lib/postgresql stop
```

---

## 🔧 Полезные команды для всех сценариев

### Проверка портов
```bash
# Посмотреть все занятые порты
netstat -tlnp | grep LISTEN

# Найти процесс на порту 5000
lsof -i :5000

# Освободить порт
fuser -k 5000/tcp
```

### Управление процессами
```bash
# Все Python процессы
ps aux | grep python

# Убить все Python процессы
pkill -f python

# Убить процесс по PID
kill -9 <PID>

# Убить процесс по имени
pkill -f registry_service
```

### Логирование
```bash
# Запуск с логированием
python service.py > service.log 2>&1 &

# Просмотр логов
tail -f service.log

# Поиск ошибок
grep -i error service.log

# Последние 50 строк
tail -n 50 service.log
```

### Мониторинг
```bash
# Использование CPU и RAM
top

# Использование RAM
free -h

# Использование диска
df -h

# Процессы Python
ps aux | grep python | awk '{print $2, $3, $4, $11}'
```

### Проверка всех портов одной командой
```bash
for port in 5000 5001 5002 5003 5004 5005 5999; do
  echo -n "Port $port: "
  curl -s http://127.0.0.1:$port/health > /dev/null && echo "✅ OK" || echo "❌ DOWN"
done
```

---

## 📱 Flutter приложение

### Сборка APK
```bash
cd ~/daten30/hub-portal/flutter-hub
bash build-apk.sh
```

### Установка APK
```bash
# Через ADB
adb install build/app/outputs/flutter-apk/app-release.apk

# Через файловый менеджер
cp build/app/outputs/flutter-apk/app-release.apk ~/storage/downloads/
# Затем открыть в File Manager и установить
```

### Проверка Flutter
```bash
flutter doctor
flutter --version
```

---

## 💾 Работа с базами данных

### SQLite (Hub Portal)
```bash
# Открыть БД Registry
sqlite3 ~/daten30/hub-portal/infrastructure/registry-service/services.db

# Команды SQLite:
.tables                          # Список таблиц
SELECT * FROM services;          # Все сервисы
SELECT * FROM events;            # События
.exit                            # Выход
```

### PostgreSQL (Production)
```bash
# Подключение
psql -U postgres -d hub_portal_db

# SQL команды:
\dt                              # Список таблиц
SELECT * FROM services;          # Все сервисы
\q                               # Выход

# Резервная копия
pg_dump -U postgres hub_portal_db > backup.sql

# Восстановление
psql -U postgres hub_portal_db < backup.sql
```

### Redis (Production)
```bash
# Подключение
redis-cli

# Redis команды:
PING                             # Проверка
KEYS *                           # Все ключи
GET key_name                     # Получить значение
SET key_name value               # Установить значение
DEL key_name                     # Удалить
FLUSHALL                         # Очистить всё
EXIT                             # Выход
```

---

## 🔄 Git команды

### Клонирование репозитория
```bash
cd ~
git clone <URL> daten30
cd daten30
```

### Обновление кода
```bash
cd ~/daten30
git pull origin main
```

### Переключение веток
```bash
git checkout claude/web-tech-overview-cNWb5
```

---

## ⚡ Автозапуск при старте Termux

### Для Hub Portal
```bash
echo 'cd ~/daten30/hub-portal && bash scripts/start-all.sh' >> ~/.bashrc
```

### Для Production
```bash
echo 'bash ~/daten30/start-production.sh' >> ~/.bashrc
```

### Отключить автозапуск
```bash
nano ~/.bashrc
# Удалить строку с автозапуском
```

---

## 🧪 Тестирование API

### Создание продукта
```bash
curl -X POST http://127.0.0.1:5001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "Description",
    "price": 100,
    "stock": 10,
    "category": "electronics"
  }' | jq
```

### Получение продукта
```bash
curl http://127.0.0.1:5001/api/products/1 | jq
```

### Обновление продукта
```bash
curl -X PUT http://127.0.0.1:5001/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product",
    "price": 150
  }' | jq
```

### Удаление продукта
```bash
curl -X DELETE http://127.0.0.1:5001/api/products/1 | jq
```

---

## 📊 Сравнение команд

| Операция | Demo-App | Hub Portal | Production |
|----------|----------|------------|------------|
| **Установка** | `pkg install python git` | `pkg install python git sqlite` | `pkg install python postgresql redis nginx` |
| **Запуск** | Вручную каждый сервис | `bash scripts/start-all.sh` | `bash start-production.sh` |
| **Остановка** | `pkill -f python` | `bash scripts/stop-all.sh` | `pkill -f gunicorn; nginx -s stop; ...` |
| **Проверка** | `curl` каждый порт | `bash scripts/health-check.sh` | `ps aux \| grep gunicorn` |
| **Логи** | `print()` | `print()` | `tail -f /var/log/nginx/error.log` |

---

## 🎯 Быстрый старт (одна команда)

### Demo-App
```bash
pkg install python git -y && pip install flask flask-cors && cd ~/daten30/demo-app/backend-flask/user-service && python user_service.py & cd ../product-service && python product_service.py & cd ../order-service && python order_service.py &
```

### Hub Portal (РЕКОМЕНДУЕТСЯ)
```bash
pkg install python git sqlite jq -y && pip install flask flask-cors requests && cd ~/daten30/hub-portal && bash scripts/start-all.sh
```

### Production
```bash
pkg install python postgresql redis nginx -y && pip install flask gunicorn psycopg2-binary redis && initdb $PREFIX/var/lib/postgresql && pg_ctl -D $PREFIX/var/lib/postgresql start && createdb hub_portal_db && bash ~/daten30/start-production.sh
```

---

## 📚 Документация

| Сценарий | Основная документация |
|----------|----------------------|
| **Demo-App** | `demo-app/README.md` |
| **Hub Portal** | `hub-portal/README.md`, `DYNAMIC_HUB_METHODOLOGY.md` |
| **Production** | `DEVELOPER_GUIDE.md`, `STACK_COMPARISON.md` |
| **Termux** | `TERMUX_SETUP_GUIDE.md`, `TERMUX_QUICK_START.md` |
| **Структура** | `PROJECT_STRUCTURE.md` |

---

## 🆘 Troubleshooting

### Порт уже занят
```bash
# Найти процесс
lsof -i :5000

# Убить процесс
fuser -k 5000/tcp

# Или изменить порт в коде
nano service.py
# Изменить PORT = 5001
```

### Не хватает памяти
```bash
# Проверить использование
free -h

# Убить лишние процессы
pkill -f chrome
pkill -f node

# Запустить только необходимые сервисы
```

### Сервис не регистрируется
```bash
# Проверить что Registry запущен
curl http://127.0.0.1:5000/api/services

# Проверить логи сервиса
tail -f service.log

# Перезапустить Registry
pkill -f registry_service
cd ~/daten30/hub-portal/infrastructure/registry-service
python registry_service.py &
```

### База данных не работает
```bash
# SQLite: проверить файл
ls -lh *.db

# PostgreSQL: проверить статус
pg_ctl status

# PostgreSQL: перезапуск
pg_ctl restart

# Redis: проверка
redis-cli ping
```

---

**Последнее обновление:** 2026-01-06
**Версия:** 1.0
**Проект:** daten30 Hub Portal
