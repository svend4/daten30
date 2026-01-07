# GitHub Repository - Информация о репозитории

## 📍 Полный адрес репозитория

```
https://github.com/svend4/daten30
```

## 📦 Клонирование в Termux

### Вариант 1: Простое клонирование

```bash
cd ~
git clone https://github.com/svend4/daten30.git
cd daten30
```

### Вариант 2: Клонирование с указанием имени директории

```bash
cd ~
git clone https://github.com/svend4/daten30.git daten30
cd daten30
```

### Вариант 3: Клонирование только последнего коммита (быстрее)

```bash
cd ~
git clone --depth 1 https://github.com/svend4/daten30.git
cd daten30
```

## 🔧 Полная установка для Termux

### Демо-приложение

```bash
# Установка зависимостей
pkg update && pkg upgrade -y
pkg install python git -y
pip install flask flask-cors

# Клонирование репозитория
cd ~
git clone https://github.com/svend4/daten30.git
cd daten30/demo-app/backend-flask

# Запуск сервисов
cd user-service && python user_service.py &
cd ../product-service && python product_service.py &
cd ../order-service && python order_service.py &

# Проверка
sleep 3
curl http://127.0.0.1:5001/api/users
curl http://127.0.0.1:5002/api/products
curl http://127.0.0.1:5003/api/orders
```

### Hub Portal (РЕКОМЕНДУЕТСЯ)

```bash
# Установка зависимостей
pkg update && pkg upgrade -y
pkg install python git sqlite jq -y
pip install flask flask-cors requests

# Клонирование репозитория
cd ~
git clone https://github.com/svend4/daten30.git
cd daten30/hub-portal

# Автоматический запуск
bash scripts/start-all.sh

# Проверка здоровья
sleep 5
bash scripts/health-check.sh
```

## 🌐 Веб-интерфейс GitHub

Открыть в браузере: **https://github.com/svend4/daten30**

## 📥 Скачивание ZIP-архива (без git)

Если Git не установлен, можно скачать ZIP:

```bash
# Установка wget
pkg install wget unzip -y

# Скачивание архива
cd ~
wget https://github.com/svend4/daten30/archive/refs/heads/main.zip

# Распаковка
unzip main.zip
mv daten30-main daten30
cd daten30
```

## 🔄 Обновление репозитория

Если репозиторий уже склонирован:

```bash
cd ~/daten30
git pull origin main
```

## 📋 Проверка текущей ветки и статуса

```bash
cd ~/daten30

# Текущая ветка
git branch

# Статус изменений
git status

# История коммитов
git log --oneline -10
```

## 🛠️ Устранение проблем

### Проблема: "fatal: destination path 'daten30' already exists"

Решение:
```bash
cd ~
rm -rf daten30  # Удалить старую папку
git clone https://github.com/svend4/daten30.git
```

### Проблема: "Permission denied"

Решение:
```bash
chmod +x ~/daten30/hub-portal/scripts/*.sh
```

### Проблема: Git не установлен

Решение:
```bash
pkg install git -y
```

## 📚 Дополнительная документация

После клонирования доступны файлы:

- **TERMUX_SETUP_GUIDE.md** - Подробное руководство по установке
- **TERMUX_QUICK_START.md** - Быстрые команды (копи-паста)
- **BUILD_HUB_APP.md** - Как собрать Flutter APK
- **FLUTTER_APPS_COMPARISON.md** - Сравнение вариантов приложений
- **hub-portal/README.md** - Документация Hub Portal

## 🎯 Все три сценария

1. **Демо-приложение** (~/daten30/demo-app) - простой вариант, 3 сервиса
2. **Hub Portal** (~/daten30/hub-portal) - продвинутый, динамическое обнаружение
3. **Продакшн** - полная инфраструктура с мониторингом

## 📞 Поддержка

- **Issues**: https://github.com/svend4/daten30/issues
- **Pull Requests**: https://github.com/svend4/daten30/pulls
- **Wiki**: https://github.com/svend4/daten30/wiki (если доступно)

---

**Последнее обновление**: 2026-01-07
**Репозиторий**: svend4/daten30
**Лицензия**: см. LICENSE файл в репозитории
