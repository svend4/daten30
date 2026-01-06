# 🚀 Quick Start Guide - Dynamic Hub Portal

Этот гайд поможет запустить Dynamic Hub Portal за 5 минут.

---

## ⚡ Быстрый старт (для опытных)

```bash
cd ~/daten30/hub-portal
bash scripts/start-all.sh
bash scripts/health-check.sh
```

Готово! Все сервисы запущены.

---

## 📋 Пошаговый запуск (для начинающих)

### Шаг 1: Установить зависимости

```bash
# В Termux
pkg install python
pip install flask requests
```

### Шаг 2: Перейти в директорию проекта

```bash
cd ~/daten30/hub-portal
```

### Шаг 3: Запустить все сервисы

```bash
bash scripts/start-all.sh
```

Вы увидите:
```
==================================================
🚀 Starting Dynamic Hub Portal
==================================================

Step 1: Starting Infrastructure Services
--------------------------------------------------
Starting Service Registry (port 5000)... ✓ PID: 12345
Starting Message Bus (port 5999)... ✓ PID: 12346

Step 2: Starting Microservices
--------------------------------------------------
Starting Product Service (port 5001)... ✓ PID: 12347
Starting Weather Service (port 5002)... ✓ PID: 12348
Starting Crypto Service (port 5003)... ✓ PID: 12349
Starting News Service (port 5004)... ✓ PID: 12350
Starting Task Service (port 5005)... ✓ PID: 12351

==================================================
✅ All services started successfully!
==================================================
```

### Шаг 4: Проверить статус

```bash
bash scripts/health-check.sh
```

Результат:
```
Infrastructure Services:
--------------------------------------------------
Service Registry    (port 5000): ✅ healthy
Message Bus         (port 5999): ✅ healthy

Microservices:
--------------------------------------------------
Product Service     (port 5001): ✅ healthy
Weather Service     (port 5002): ✅ healthy
Crypto Service      (port 5003): ✅ healthy
News Service        (port 5004): ✅ healthy
Task Service        (port 5005): ✅ healthy

Summary: 7/7 services running
✅ All services are healthy
```

---

## 🧪 Тестирование сервисов

### Проверить Service Registry

```bash
curl http://127.0.0.1:5000/api/services
```

Ответ:
```json
{
  "success": true,
  "services": [
    {
      "id": "product-service",
      "name": "Товары",
      "port": 5001,
      "status": "active",
      "icon": "shopping_cart",
      "color": "#4CAF50"
    },
    ...
  ],
  "total": 5
}
```

### Проверить Product Service

```bash
curl http://127.0.0.1:5001/api/products
```

### Проверить Weather Service

```bash
curl http://127.0.0.1:5002/api/weather/current
```

### Проверить Crypto Service

```bash
curl http://127.0.0.1:5003/api/crypto/prices
```

---

## 🛑 Остановка сервисов

```bash
bash scripts/stop-all.sh
```

Вывод:
```
Stopping Task Service... ✓ Stopped
Stopping News Service... ✓ Stopped
Stopping Crypto Service... ✓ Stopped
Stopping Weather Service... ✓ Stopped
Stopping Product Service... ✓ Stopped
Stopping Message Bus... ✓ Stopped
Stopping Service Registry... ✓ Stopped
```

---

## 📱 Установка Flutter приложения

### Вариант 1: Использовать готовый APK

1. Скачать APK из GitHub Actions
2. Установить на устройство: `adb install app-release.apk`

### Вариант 2: Собрать самостоятельно

```bash
cd flutter-hub
flutter build apk --release
```

APK будет в: `build/app/outputs/flutter-apk/app-release.apk`

---

## 🔍 Отладка

### Просмотр логов

```bash
# Все логи
ls ~/termux-backend/logs/

# Конкретный сервис
tail -f ~/termux-backend/logs/product.log
```

### Проверка портов

```bash
# Посмотреть какие порты заняты
netstat -tuln | grep LISTEN
```

### Перезапуск одного сервиса

```bash
# Остановить
pkill -f product_service.py

# Запустить
python microservices/product-service/product_service.py
```

---

## ❓ Частые проблемы

### Проблема: "Address already in use"

**Причина:** Порт уже занят другим процессом

**Решение:**
```bash
# Найти процесс
lsof -i :5001

# Убить процесс
kill -9 <PID>
```

### Проблема: "Connection refused"

**Причина:** Сервис не запущен

**Решение:**
```bash
bash scripts/health-check.sh
bash scripts/start-all.sh
```

### Проблема: "Module not found: flask"

**Причина:** Flask не установлен

**Решение:**
```bash
pip install flask requests
```

---

## 🎯 Следующие шаги

1. ✅ Запустить все сервисы
2. ✅ Проверить health check
3. ✅ Протестировать API через curl
4. 📱 Установить Flutter приложение
5. 🎨 Создать свой микросервис

**Документация:**
- [Добавление нового сервиса](ADDING_SERVICE.md)
- [UI Schema спецификация](UI_SCHEMA.md)
- [API протокол](API_PROTOCOL.md)

---

**Happy coding! 🚀**
