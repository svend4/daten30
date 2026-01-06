# Termux Quick Start - Быстрый справочник команд

Краткие команды для быстрого запуска каждого сценария в одну копипасту.

---

## 🎯 Сценарий 1: Демо-приложение

### Полная установка и запуск (копируй целиком)

```bash
# Установка зависимостей
pkg update && pkg upgrade -y && pkg install python git -y && pip install flask flask-cors

# Запуск всех сервисов
cd ~/daten30/demo-app/backend-flask/user-service && python user_service.py &
cd ~/daten30/demo-app/backend-flask/product-service && python product_service.py &
cd ~/daten30/demo-app/backend-flask/order-service && python order_service.py &

# Проверка
sleep 3 && curl http://127.0.0.1:5001/api/users && curl http://127.0.0.1:5002/api/products && curl http://127.0.0.1:5003/api/orders
```

### Остановка

```bash
pkill -f python
```

---

## 🔌 Сценарий 2: Hub Portal (РЕКОМЕНДУЕТСЯ)

### Полная установка и запуск (копируй целиком)

```bash
# Установка зависимостей
pkg update && pkg upgrade -y && pkg install python git sqlite jq -y && pip install flask flask-cors requests

# Автоматический запуск
cd ~/daten30/hub-portal && bash scripts/start-all.sh

# Проверка здоровья
sleep 5 && bash scripts/health-check.sh
```

### Ручной запуск (если нужен контроль)

```bash
# Инфраструктура
cd ~/daten30/hub-portal/infrastructure/registry-service && python registry_service.py &
sleep 2
cd ~/daten30/hub-portal/infrastructure/message-bus && python message_bus.py &
sleep 2

# Микросервисы
cd ~/daten30/hub-portal/microservices/product-service && python product_service.py &
sleep 1
cd ~/daten30/hub-portal/microservices/weather-service && python weather_service.py &
sleep 1
cd ~/daten30/hub-portal/microservices/crypto-service && python crypto_service.py &
sleep 1
cd ~/daten30/hub-portal/microservices/news-service && python news_service.py &
sleep 1
cd ~/daten30/hub-portal/microservices/task-service && python task_service.py &

# Проверка
sleep 3 && curl http://127.0.0.1:5000/api/services | jq
```

### Остановка

```bash
cd ~/daten30/hub-portal && bash scripts/stop-all.sh
```

---

## 🚀 Сценарий 3: Production приложение

### Шаг 1: Первоначальная установка (однократно)

```bash
# Установка всех пакетов
pkg update && pkg upgrade -y
pkg install python nodejs-lts postgresql redis sqlite nginx git jq -y
pip install flask fastapi gunicorn psycopg2-binary redis requests celery uvicorn

# Настройка PostgreSQL
initdb $PREFIX/var/lib/postgresql
pg_ctl -D $PREFIX/var/lib/postgresql start
createuser -s postgres
createdb hub_portal_db

# Проверка
psql -U postgres -d hub_portal_db -c "SELECT version();"
```

### Шаг 2: Создание production скрипта

```bash
cat > ~/daten30/start-production.sh << 'SCRIPT'
#!/bin/bash
echo "🚀 Starting Production Stack..."

# Databases
pg_ctl -D $PREFIX/var/lib/postgresql start
redis-server --daemonize yes
sleep 3

# Nginx
nginx

# Infrastructure
cd ~/daten30/hub-portal/infrastructure/registry-service
gunicorn -w 4 -b 127.0.0.1:5000 registry_service:app --daemon
cd ~/daten30/hub-portal/infrastructure/message-bus
gunicorn -w 4 -b 127.0.0.1:5999 message_bus:app --daemon
sleep 3

# Microservices
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
echo "📊 Registry: http://127.0.0.1:5000/api/services"
echo "🌐 Nginx proxy: http://127.0.0.1:8080"
SCRIPT

chmod +x ~/daten30/start-production.sh
```

### Шаг 3: Запуск production

```bash
bash ~/daten30/start-production.sh
```

### Шаг 4: Проверка

```bash
# Проверка всех процессов
ps aux | grep -E "gunicorn|nginx|postgres|redis" | grep -v grep

# Проверка сервисов
curl http://127.0.0.1:5000/api/services | jq
curl http://127.0.0.1:8080/registry/api/services | jq

# Проверка баз данных
redis-cli ping
psql -U postgres -d hub_portal_db -c "SELECT COUNT(*) FROM services;"
```

### Остановка production

```bash
pkill -f gunicorn
nginx -s stop
redis-cli shutdown
pg_ctl -D $PREFIX/var/lib/postgresql stop
```

---

## 📊 Какой сценарий выбрать?

```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│                 │ Демо-app     │ Hub Portal   │ Production   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Время установки │ 5 минут      │ 10 минут     │ 30+ минут    │
│ Сложность       │ ⭐           │ ⭐⭐         │ ⭐⭐⭐⭐     │
│ RAM             │ ~100 MB      │ ~200 MB      │ ~500 MB      │
│ Возможности     │ Базовые      │ Расширенные  │ Максимальные │
│ Для обучения    │ ✅           │ ✅           │ ❌           │
│ Для production  │ ❌           │ ⚠️           │ ✅           │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

**Рекомендация:** Начните с **Hub Portal** (сценарий 2)

---

## 🔥 Супер-быстрый старт (Hub Portal за 30 секунд)

Если у вас уже установлен Termux с Python:

```bash
# Одна команда для запуска всего!
cd ~/daten30/hub-portal && bash scripts/start-all.sh && sleep 3 && bash scripts/health-check.sh
```

Если Termux чистый:

```bash
# Установка + запуск одной командой
pkg update -y && pkg install python git -y && pip install flask flask-cors requests && cd ~/daten30/hub-portal && bash scripts/start-all.sh
```

---

## 🛠️ Полезные однострочные команды

### Проверка всех портов

```bash
for port in 5000 5001 5002 5003 5004 5005 5999; do echo -n "Port $port: "; curl -s http://127.0.0.1:$port/health > /dev/null && echo "✅ OK" || echo "❌ DOWN"; done
```

### Остановка всех сервисов

```bash
pkill -f python; pkill -f gunicorn; pkill -f node; nginx -s stop 2>/dev/null; redis-cli shutdown 2>/dev/null; pg_ctl stop 2>/dev/null
```

### Просмотр всех запущенных сервисов

```bash
ps aux | grep -E "python|node|nginx|redis|postgres" | grep -v grep | awk '{print $11, $12, $13}'
```

### Проверка памяти

```bash
free -h && echo "---" && ps aux | grep -E "python|node|nginx|redis|postgres" | awk '{sum+=$6} END {print "Services using: " sum/1024 " MB"}'
```

### Автозапуск Hub Portal при старте Termux

```bash
echo 'cd ~/daten30/hub-portal && bash scripts/start-all.sh' >> ~/.bashrc
```

---

## 🎓 Обучающие команды

### Посмотреть что происходит в Service Registry

```bash
# Список всех зарегистрированных сервисов
curl http://127.0.0.1:5000/api/services | jq '.services[] | {name, port, status}'

# История событий
curl http://127.0.0.1:5000/api/events | jq '.events[] | {type, service_id, timestamp}'
```

### Посмотреть события в Message Bus

```bash
# Все события
curl http://127.0.0.1:5999/api/events | jq

# Подписки
curl http://127.0.0.1:5999/api/subscriptions | jq
```

### Тестирование Product Service

```bash
# Получить все продукты
curl http://127.0.0.1:5001/api/products | jq

# Создать новый продукт
curl -X POST http://127.0.0.1:5001/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":100,"stock":10}' | jq

# Получить продукт по ID
curl http://127.0.0.1:5001/api/products/1 | jq
```

### Проверка работы динамического обнаружения

```bash
# 1. Запустить Hub Portal
cd ~/daten30/hub-portal && bash scripts/start-all.sh

# 2. Проверить сколько сервисов зарегистрировано
curl http://127.0.0.1:5000/api/services | jq '.services | length'

# 3. Остановить один сервис
pkill -f weather_service

# 4. Подождать 30 секунд и проверить снова
sleep 30 && curl http://127.0.0.1:5000/api/services | jq '.services | length'
```

---

## 📱 Подключение Flutter приложения

После запуска Hub Portal в Termux:

```bash
# 1. Запустить Hub Portal
cd ~/daten30/hub-portal && bash scripts/start-all.sh

# 2. Проверить что Registry работает
curl http://127.0.0.1:5000/api/services

# 3. Установить Flutter APK на телефон
cd ~/daten30/hub-portal/flutter-hub
bash build-apk.sh

# 4. Установить APK
adb install build/app/outputs/flutter-apk/app-release.apk

# Приложение автоматически найдет все сервисы!
```

---

## ⚡ Troubleshooting одной командой

### Если ничего не работает

```bash
# Полная перезагрузка
pkill -f python; sleep 2; cd ~/daten30/hub-portal && bash scripts/start-all.sh && sleep 5 && bash scripts/health-check.sh
```

### Если порт занят

```bash
# Освободить порт 5000
fuser -k 5000/tcp

# Проверить что порт свободен
netstat -tlnp | grep 5000
```

### Если не хватает памяти

```bash
# Запустить только инфраструктуру + 2 сервиса
cd ~/daten30/hub-portal/infrastructure/registry-service && python registry_service.py &
sleep 2
cd ~/daten30/hub-portal/infrastructure/message-bus && python message_bus.py &
sleep 2
cd ~/daten30/hub-portal/microservices/product-service && python product_service.py &
cd ~/daten30/hub-portal/microservices/weather-service && python weather_service.py &
```

---

## 🎯 Рекомендованный workflow

### Ежедневная работа с Hub Portal

```bash
# Утро: запуск
cd ~/daten30/hub-portal && bash scripts/start-all.sh

# Разработка: проверка логов
tail -f /tmp/registry.log

# Вечер: остановка
bash scripts/stop-all.sh
```

### Разработка нового микросервиса

```bash
# 1. Создать новый сервис
cd ~/daten30/hub-portal/microservices
mkdir my-service && cd my-service

# 2. Скопировать шаблон
cp ../product-service/product_service.py my_service.py

# 3. Изменить порт и логику
nano my_service.py

# 4. Запустить
python my_service.py &

# 5. Проверить регистрацию
curl http://127.0.0.1:5000/api/services | jq '.services[] | select(.id=="my-service")'
```

---

## 📖 Дополнительные ресурсы

- **Полное руководство:** `TERMUX_SETUP_GUIDE.md`
- **Методология:** `DEVELOPER_GUIDE.md`
- **Архитектура Hub Portal:** `hub-portal/README.md`
- **Flutter приложение:** `hub-portal/flutter-hub/README.md`

---

**Совет:** Сохраните этот файл в закладки для быстрого доступа к командам! 🔖
