#!/data/data/com.termux/files/usr/bin/bash
# Автоматическая установка и настройка Flask backend в Termux

echo "🔧 Установка Flask Backend для Termux"
echo "======================================"

# Проверка что мы в Termux
if [ ! -d "$PREFIX" ]; then
    echo "❌ Ошибка: Этот скрипт должен запускаться в Termux!"
    exit 1
fi

echo ""
echo "📦 Шаг 1/6: Обновление пакетов..."
pkg update -y
pkg upgrade -y

echo ""
echo "📦 Шаг 2/6: Установка необходимых пакетов..."
pkg install -y python python-pip git wget curl nano

echo ""
echo "📦 Шаг 3/6: Установка Python библиотек..."
pip install --upgrade pip
pip install flask

echo ""
echo "📁 Шаг 4/6: Создание структуры папок..."
mkdir -p ~/termux-backend/{logs,data,scripts}

echo ""
echo "📥 Шаг 5/6: Клонирование репозитория..."
if [ -d ~/daten30 ]; then
    echo "⚠️  Репозиторий уже существует, обновляем..."
    cd ~/daten30
    git pull
else
    cd ~
    git clone https://github.com/svend4/daten30.git
fi

echo ""
echo "✅ Шаг 6/6: Копирование сервисов..."
cp -r ~/daten30/demo-app/services ~/termux-backend/

echo ""
echo "✅ Установка завершена!"
echo ""
echo "Следующие шаги:"
echo "1. Запустите: ~/termux-backend/scripts/start-all.sh"
echo "2. Проверьте: curl http://localhost:5001/health"
echo "3. Откройте Flutter App"
echo ""
echo "📚 Документация: ~/daten30/demo-app/TERMUX_SETUP.md"
